from System.Entities import Email, Person, Phone
from System.Entities.Organization import *
#from Connectors.Connector import Connector
from System.Entities.Person import GetNameFromGoogleContactsStrategy
from System.EntityToDatabase import PersonToDatabase

#Have to install through pip install requests/facepy
from facepy import *
import requests
import json

ACCESS_TOKEN = "CAADaQW5ft88BALCNSBmoDFXGlAwXqFKmHbTnZC2R9uSvoOtcU8NoDUZBsFQZCVuOcIDyxeFIWPmCiXBCVeKdQJxH2kb6HIBTlPEYY9PxlLK8tpjvoxVp6aQgwV051lN3pKZBrjbnWQXqAM2lxJmJgc6TpwgjYNJVGnERcPaFHHv8f8BCbNbLh8ideg4OTnUZD"
class FacebookContactsConnector:
    #FACEBOOK_APP_ID = "239974559496143"
    #FACEBOOK_APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
    def __init__(self, db):
        #Willl have to hardcode access code until GUI is written
        #self.my_connector = Connector()
        self.people = []
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

    def import_user_info(self, user):
        data = self.graph.get(user)
        birthday = "Not Listed"
        if "birthday" in data:
            birthday = data["birthday"]
            print birthday
        id = data["id"]
        ##TO DO --> Build Person from Facebook
        print "Building new person..."
    # Find this precondition if necessary
    def org_in_db(self, org):
        return False
    def build_education_org(self, school):
        name = school["school"]["name"]
        orgid = school["school"]["id"] + 0
        note = "From Facebook"
        org = Organization(orgid,name,note)
        if not self.org_in_db(org):
            print "Pushing to DB"
        #print education

    def import_education(self, id):
        query = "SELECT education FROM user WHERE uid="+id

        response = self.graph.fql(query)
        ##format {"education": [school_1: properties][school_2: properties]
        education = response["data"][0]
        #print education

        return education

    def friends_to_db(self):
        print "TO DO"



    def run(self):
        #print self.graph.get('me') #returns node rather than database table
        id = self.friends[30]["id"]
        print id
        self.import_user_info(id)
        education = self.import_education(id)
        school = education["education"][0]
        print school
        #school = education[]
        self.build_education_org(school)
        #print friends["data"]
       #store temp copy of graph
      # print self.graph.get('me/posts')

f = FacebookContactsConnector("db_temp")
f.run()