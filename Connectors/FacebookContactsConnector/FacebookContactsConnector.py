from System.Entities import Email, Person, Phone, Message
from System.Entities.Organization import *
#from Connectors.Connector import Connector
#from System.Entities.Person import GetNameFromGoogleContactsStrategy
from System.Entities.Person import GetNameFromFacebookContactsStrategy
from System.EntityToDatabase import PersonToDatabase

#Have to install through pip install requests/facepy
from facepy import *
import datetime

ACCESS_TOKEN = "CAACEdEose0cBAFq0PSJ4dDeOZAsm3hkh2SHwDCUkZCx8UcRaxfoyah1RbW2RfRCLsadqNR0oJnyGWm5dG4A2gtGrnJiMtKf44ovOL39LnCq61XNZCvWTylBsy7GXtEyzxOtqdsqHXSFrDdCrdEh6EENKrqp9F5xwHpYkhFhrOS0xmuDM3qWECeg5yDHZASgZD"
LIMIT = 3
APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
class FacebookContactsConnector:
    #FACEBOOK_APP_ID = "239974559496143"
    #FACEBOOK_APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
    def __init__(self, db):
        #Willl have to hardcode access code until GUI is written
        #self.my_connector = Connector()
        self.contacts = [] #will be processed from raw friends
        self.db = db
        self.app_id = 239974559496143
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

    #build a new person for all contacts. push the friends that aren't in db to db
    def process_friends(self):
        count = 0;
        for f in self.friends:
            id = f["id"]
            friend = self.graph.get(id)
            p = self.build_person(friend)
            self.contacts.append(p)
            #pass full education history in
            if "education" in friend:
                self.process_education(friend["education"])
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
        query = "SELECT message_id, body, created_time FROM message WHERE thread_id="+thread_id
        raw_conversation = self.graph.fql(query)["data"] #the entire conversation on that thread
        print raw_conversation
        #has body, created_time, and message_id
        for m in raw_conversation:
            message = self.build_message(m)
            conversation.append(message)

        return conversation

    #converts json message to Entities.Message object
    def build_message(self, m):
        body = m["body"]
        id = m["message_id"]
        #convert from unix time stamp
        time_stamp = self.get_time(m["created_time"])
        message = Message.Message(id, body, time_stamp)
        return message

    def get_time(self, unix_time):
        str_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')
        return str_time


    def run(self):
       # self.process_friends()
        print self.message_threads
        self.process_messages()
        print str(self.message_threads)


f = FacebookContactsConnector("db_temp")
f.run()