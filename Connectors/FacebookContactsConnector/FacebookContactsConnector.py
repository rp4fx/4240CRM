from System.Entities import EmailMessage, Person, Phone, Message
from System.Entities.Organization import *
#from Connectors.Connector import Connector
#from System.Entities.Person import GetNameFromGoogleContactsStrategy
from System.Entities.Person import GetNameFromFacebookContactsStrategy
from System.EntityToDatabase import PersonToDatabase

#Have to install through pip install requests/facepy
from facepy import *
import datetime

ACCESS_TOKEN = "CAADaQW5ft88BAA0e4cHSfNMJSKrEfQGnE5dFVRzwgO1AhXrf51mFhrVb8v9jWvepGUO2muZAcRHGWRjZAGua5ZAWoUeP4OTtOn0Kl8jyMulqKVB0XpuKWejBmXDR6UdxFzZByeDK8A6PaGpGjPZBQspjixxaa9oZCfi3T0kjBzZB8IPszJOCetReLuX5N9Cc0YZD"
LIMIT = 5
APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
APP_ID = 239974559496143
class FacebookContactsConnector:

    def __init__(self, db):
        #Willl have to hardcode access code until GUI is written
        #self.my_connector = Connector()
        self.contacts = {} #"Firstname LastName": Person Object
        self.db = db
        self.app_id = APP_ID
        self.app_secret = APP_SECRET
        self.access_token = ACCESS_TOKEN
        #token, date = get_extended_access_token(self.access_token, self.app_id, self.app_secret)
        self.graph = GraphAPI(self.access_token)
        self.friends = self.import_friends()
        self.message_threads = [] #initialized from process_messages

    ##Rebuilds gets copy of graph locally
    def import_friends(self):
        friends = self.graph.get("me/friends")
        return friends["data"]

    #returns a dict of person formatted data ["birthday": bd, "gender": m/f"]
    def get_user_info(self, user):
        birthday = "Not Listed"
        if "birthday" in user:
            birthday = user["birthday"]
        gender = ""
        if "gender" in user:
            gender = user["gender"]
        return {"gender": gender, "birthday": birthday}

    def build_education_org(self, school):
        name = school["school"]["name"]
        orgid = school["school"]["id"]
        note = "From Facebook"
        org = Organization(orgid,name,note)
        return org

    def build_person_from_id(self, id):
        user = self.graph.get(str(id))
        person = self.build_person(user)
        return person

    #build a new person for all contacts. push the friends that aren't in db to db
    def process_friends(self):
        count = 0;
        for f in self.friends:
            id = f["id"]
            friend = self.build_person_from_id(id)
            name = friend.get_name()
            self.contacts[name] = friend
            #pass full education history in
            #if "education" in friend:
              #  self.process_education(friend["education"])
            #Limited for purposes of testing
            count += 1
            if count > LIMIT:
                return
    def build_person(self, friend):
        info = self.get_user_info(friend)
        #check for organization
        p = Person.Person()
        fb_strategy = GetNameFromFacebookContactsStrategy(friend)
        p.add_name_from_service(fb_strategy)
        p.birthday = info["birthday"]
        p.gender = info["gender"]
        return p

    def process_education(self, education):
        for school in education:
            org = self.build_education_org(school)
            self.push_org_db(org)

    def org_in_db(self, org):
        return False
    #True if pushed, False if already in DB
    def push_org_db(self, org):
        if self.org_in_db(org):
            return False
        else:
            print "TO DO: PUSHING TO DB:", org
            return True

    def person_in_db(self, person):
        return False

    #True if pushed; False otherwise
    def push_person_db(self, person):
        if self.person_in_db(person):
            return False
        else:
            # print "TO DO: PUSHING TO DB:", person
            return True

    def process_messages(self):
        threads = []
        #folder_id = 0 === Inbox
        query = "SELECT thread_id FROM thread WHERE folder_id=0"
        inbox = self.graph.fql(query)["data"]
        #print inbox
        count = 0
        for thread in inbox:
            thread_id = thread["thread_id"]
            conversation = self.get_conversation(thread_id)
            self.message_threads.append(conversation)
            count += 1
            if count > LIMIT:
                return
    #returns a list of processed messages from the given thread_id
    def get_conversation(self, thread_id):
        conversation = []
        query = "SELECT message_id, body, created_time, author_id FROM message WHERE thread_id="+thread_id
        raw_conversation = self.graph.fql(query)["data"] #the entire conversation on that thread
        #must determine who is viewer_id. if the from == viewer_id, then the to == the other
        conversant_ids = self.get_conversant_ids(raw_conversation)
       # print raw_conversation
        for m in raw_conversation:
            message = self.build_message(m, conversant_ids)
            conversation.append(message)

        return conversation

    def get_conversant_ids(self, raw_conversation):
        owner_id = self.graph.get("me")["id"]
        for message in raw_conversation:
            if not message["author_id"] == owner_id:
                return {"owner_id": owner_id, "friend_id": message["author_id"]}
        #never reached
        return {"owner_id": owner_id, "friend_id": ""}


    #converts json message to Entities.Message object
    def build_message(self, m, conversant_ids):
        body = m["body"]
        id = m["message_id"]
        time_stamp = self.get_time(m["created_time"])
        message = Message.Message(id, body, time_stamp)
        information = self.get_message_information(m, conversant_ids, message)
        message.set_people(information)
        return message

    def get_message_information(self, m, conversant_ids, message):
        from_id = m["author_id"]
        person_from = self.person_from_contacts(from_id)
        person_from.add_message(message)
        to_id = self.get_recipient(from_id, conversant_ids)
        person_to = self.person_from_contacts(to_id)
        person_to.add_message(message)
        information = {"TO": person_to, "FROM": person_from, "CC": "", "BCC": ""}
        return information

    #Check for person in contacts, if not, add them to contact list
    def person_from_contacts(self, id):
        person = self.build_person_from_id(id)
        name = person.get_name()
        if name in self.contacts:
            #print name + " in contacts"
            person = self.contacts[name]
        else:
            #print "MESSAGE FROM NEW CONTACT"
            self.contacts[name] = person

        return person

    def get_recipient(self, from_id, conversant_ids):
        if from_id == conversant_ids["owner_id"]:
            return conversant_ids["friend_id"]
        else:
            return conversant_ids["owner_id"]

    def get_time(self, unix_time):
        str_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')
        return str_time

    def add_contacts_to_db(self):
        entity_to_database = PersonToDatabase(self.people, self.db)
        entity_to_database.add_standard_attribute_table_setters()
        entity_to_database.add_people_to_database()


    def update_contacts_for_conversations(self, conversation, person_to, person_from):
        name_to = person_to.get_name()
        print name_to in self.contacts


    def run(self):
        #Get All information Locally
        self.process_friends()
        #print self.contacts
        self.process_messages()

        for person in self.contacts:
            messages = self.contacts[person].messages
            for m in messages:
                print self.contacts[person].get_name()
                print m

f = FacebookContactsConnector("personal_graph.db")
f.run()