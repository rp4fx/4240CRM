__author__ = 'Timur'
from Connectors.GoogleContactsConnector import GoogleContactsConnector

conn = GoogleContactsConnector.GoogleContactsConnector("./personal_graph.db")
conn.run()
