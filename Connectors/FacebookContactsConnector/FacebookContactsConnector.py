from System.Entities import Email, Person, Phone
#from Connectors.Connector import Connector
from System.Entities.Person import GetNameFromGoogleContactsStrategy
from System.EntityToDatabase import PersonToDatabase

#Have to install through pip install requests/facepy
from facepy import *
import requests
import json

ACCESS_TOKEN = "CAADaQW5ft88BAPYZCViaMwqlZAqm5MyXZCDoI33ekT4Qdjz5r5yffLxgQ5gD9GlAWEq5o63uE9KMpZChuMQ46cInZA5WTsNFG6zGZCSGBGeRnlFq4oX0esPr4nMZBjZAhvLSZChTrNeQ0HQOYaZArmavDglA5LyJKeYmAZCBsLqZCz23lc12LxlZBG8s0Eza12LSYXYgZD"
class FacebookContactsConnector:
    #FACEBOOK_APP_ID = "239974559496143"
    #FACEBOOK_APP_SECRET = "eec6ae1b9b6445375c03cb9624f7b49f"
    def __init__(self):
        #Willl have to hardcode access code until GUI is written
        #self.my_connector = Connector()
        self.people = []
        self.app_id = 239974559496143
        self.app_secret = "eec6ae1b9b6445375c03cb9624f7b49f"
        self.access_token = ACCESS_TOKEN
        #token, date = get_extended_access_token(self.access_token, self.app_id, self.app_secret)
        self.graph = GraphAPI(self.access_token)

        #self.db = db
    ##Queries functional. Need to build queries to get friends/etc
    def query(self):
       print self.graph.fql("SELECT name FROM user WHERE uid = me()")

    def test_operation(self):
        print self.graph.get('me') #returns node rather than database table
        self.query()
        #print friends["data"]
       #store temp copy of graph
      # print self.graph.get('me/posts')

f = FacebookContactsConnector()
f.test_operation()