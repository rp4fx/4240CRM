from System.Entities import Email, Person, Phone
from System.Entities.Organization import *
#from Connectors.Connector import Connector
#from System.Entities.Person import GetNameFromGoogleContactsStrategy
from System.Entities.Person import GetNameFromFacebookContactsStrategy
from System.EntityToDatabase import PersonToDatabase

#Have to install through pip install requests/facepy
from facepy import *
import requests
import json

ACCESS_TOKEN = "CAADaQW5ft88BAHdDV72yFs5gt3W9yB0jGzh2NxRL0LfciTkBzBYZCEhtBcmMKXLhAZA2k9etV2yoT4upWjeDKUbWyjsAAyMsZBhyJ8gV8vXXkVSFSmQP4E8yg78QQURCRh3rZCGPtwmnjEIZAHYsyjH3xvJw4xCniM2skESWD1DL3f76XYUhOcndCnBxonFsZD"
LIMIT = 3
class FacebookContactsConnector:
    #FACEBOOK_APP_ID = "239974559496143"
    #FACEBOOK_APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
    def __init__(self, db):
        #Willl have to hardcode access code until GUI is written
        #self.my_connector = Connector()
        self.contacts = [] #will be processed into friends
        self.db = db
        self.app_id = 239974559496143
        self.app_secret = "eec6ae1b9b6445375c03cb9624f7b49f"
        self.access_token = ACCESS_TOKEN
        #token, date = get_extended_access_token(self.access_token, self.app_id, self.app_secret)
        self.graph = GraphAPI(self.access_token)
        self.friends = self.import_friends()

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
        '''if not self.org_in_db(org):
            print "Pushing to DB ", org #need to confirm with Timur for methodology
        else:
            print "Already exists!", org #confirm db code
            '''

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
            print "TO DO: PUSHING TO DB:", person
            return True

    def process_messages(self):
        print "TO DO: PROCESS MESSAGES"
    def run(self):
        self.process_friends()
        self.process_messages()

        #print friends["data"]
       #store temp copy of graph
      # print self.graph.get('me/posts')

f = FacebookContactsConnector("db_temp")
f.run()