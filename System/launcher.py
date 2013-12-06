__author__ = 'Timur'
from Connectors.GoogleContactsConnector import GoogleContactsConnector
from Connectors.FacebookContactsConnector import FacebookContactsConnector

#conn = GoogleContactsConnector.GoogleContactsConnector("./personal_graph.db")
#conn.run()
fb = FacebookContactsConnector.FacebookContactsConnector("./personal_graph.db")
fb.run()