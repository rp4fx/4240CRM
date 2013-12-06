from System.Entities import EmailMessage, Person, Phone, Message
from System.Entities.Organization import *
from System.Entities.Person import GetNameFromFacebookContactsStrategy
from System.EntityToDatabase import PersonToDatabase, FacebookMessageToDatabase

#Have to install through pip install requests/facepy
from facepy import *
import datetime

ACCESS_TOKEN = "CAADaQW5ft88BABF38Qk4eQIjt9UEv2aaHifcmfDc8uSVELQDpUqtsJkgkotiMBphmrXEpXwPfceSZCY5aVe2X9Py8sob3p2mJYZBoAurupJwgV0oYKekisb53Ebkq2IQlNNnUyYuMHF3jYgYPnMZAHARE9SbbdZBIuKWDAyeWmoKfL2YMwFlJQSLpQiU820ZD"
LIMIT = 1
APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
APP_ID = 239974559496143
class FacebookContactsConnector:

    def __init__(self, db):
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
        #check to see if
        person = self.build_person(user)
        return person

    #build a new person for all contacts. push the friends that aren't in db to db
    def process_friends(self):
        count = 0;
        for f in self.friends:
            id = f["id"]
            friend = self.build_person_from_id(id)
            key = friend.person_id
            self.contacts[key] = friend
            #pass full education history in
            #if "education" in friend:
              #  self.process_education(friend["education"])
            #Limited for purposes of testing
            count += 1
            if count > LIMIT:
                return
    def build_person(self, friend):
        info = self.get_user_info(friend)
        p = Person.Person()
        fb_strategy = GetNameFromFacebookContactsStrategy(friend)
        p.add_name_from_service(fb_strategy)
        p.birthday = info["birthday"]
        p.gender = info["gender"]
        p.person_id = self.get_person_id(p)
        return p

    def get_person_id(self, person):
        entity_to_db = PersonToDatabase([], self.db)
        entity_to_db.add_standard_attribute_table_setters()
        person_id = entity_to_db.add_person_to_database(person)
        return person_id


    def process_education(self, education):
        for school in education:
            org = self.build_education_org(school)
            self.push_org_db(org)

    def org_in_db(self, org):
        return False
    #True if pushed, False if already in DB
    '''def push_org_db(self, org):
        if self.org_in_db(org):
            return False
        else:
            print "TO DO: PUSHING TO DB:", org
            return True
    '''

    def process_messages(self):

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

        time_stamp = m["created_time"]
        message = Message.Message(id, body, time_stamp)
        information = self.get_message_information(m, conversant_ids, message)
        message.set_people(information)
        return message

    def get_message_information(self, m, conversant_ids, message):
        from_id = m["author_id"]
        person_from = self.person_from_contacts(from_id)
        to_id = self.get_recipient(from_id, conversant_ids)
        person_to = self.person_from_contacts(to_id)
        information = {"TO": [person_to], "FROM": [person_from], "CC": [], "BCC": []}
        return information

    #NEED TO SWITCH THIS.
    def person_from_contacts(self, id):
        person = self.build_person_from_id(id)
        person_id = person.person_id
        if person_id in self.contacts:
            #print name + " in contacts"
            person = self.contacts[person_id]
        else:
            #print "MESSAGE FROM NEW CONTACT"
            self.contacts[person_id] = person

        return person

    def get_recipient(self, from_id, conversant_ids):
        if from_id == conversant_ids["owner_id"]:
            return conversant_ids["friend_id"]
        else:
            return conversant_ids["owner_id"]

    def get_time(self, unix_time):
        str_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')
        return str_time

    def push_messages_to_db(self):
        print "Adding Messages to Database..."
        fb_message_db = FacebookMessageToDatabase(self.message_threads, self.db)
        fb_message_db.add_to_message_table()


    def run(self):
        #Get All information Locally
        # CURRENTLY JUST GIVES FRIENDS THAT YOU'VE FB MESSAGED RECENTLY
        # self.process_friends()

       # print self.graph.get("me")["name"]
        self.process_messages()
        self.push_messages_to_db()

        print len(self.contacts)
        '''
        for person in self.contacts:
            messages = self.contacts[person].messages
            for m in messages:
                print self.contacts[person].get_name()
                print m
        '''

#f = FacebookContactsConnector("../personal_graph.db")
#f.run()