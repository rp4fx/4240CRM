__author___ = 'Zachary'
import imaplib
import time
from datetime import date, timedelta
from System.Entities import EmailMessage, Person, Phone, Email
from Connectors.Connector import Connector
from System.Entities.EmailMessage import fillerStrategy
from System.EntityToDatabase import EmailMessageToDatabase
from System.DatabasetoEntity import DatabaseToPerson, EmailAttributeTableGetter
from System.EntityToDatabase import *


class IMAPConnector(Connector):
    def __init__(self, db):
        self.emails = []
        self.server = self.serve()
        self.username = ''
        self.password = ''
        self.email_id = ''
        self.db = db
        self.person_list =[]
        self.push_these_people_to_database = []
        self.personid_list = []
        self.messageid_list = []
        self.createp_list = []

    def serve(self):
    # try:
        return imaplib.IMAP4_SSL("imap.gmail.com", 993)

    def run(self):
        print "Starting the IMAP Connector"
        #self.serve()
        self.username = 'cs4240crm'
        self.password = 'rohantimurzach'
        #self.request_credentials()
        self.print_credentials()
        self.import_emails()
        #try:
        #   self.import_emails()
        #  self.print_emails()
        # self.add_emails_to_db()
        #except gdata.client.BadAuthentication:
        #   print 'Invalid user credentials given.'
        #  return

    def import_emails(self):
        self.login()
        e_ids = self.search(self.emailquery())
        count = 0
        for id in e_ids[0].split():
            if count > 20:
                break
            e = EmailMessage.EmailMessage()
            e.fillerStrategy.fill(self.server, id)
            e.set_message()
            self.emails.append(e)
            #feed = self.gd_client.GetContacts()
            #self.process_feed(feed, self.create_person)
            count += 1

    def check_success(self):
        for email in self.emails:
            print email.subject
            print email.timestamp
            print email.people
            print email.content

    def emailquery(self):
        t = date.today() - timedelta(days=90)
        t.replace(month=t.month - 3)
        if (t.month < 0):
            t.replace(month=12 + t.month)
        searchquery = '(SINCE "{}")'.format(t.strftime("%d-%b-%Y"))
        return searchquery

    def search(self, emailquery):
        status, e_ids = self.server.search(None, emailquery)
        return e_ids

    def login(self):
        self.server.login(self.username, self.password)
        self.server.select()
        #self.gd_client.ClientLogin(username, password, self.gd_client.source)

    def add_emails_to_database(self):
        self.find_people()
        entity_to_database = EmailMessageToDatabase(self.people, self.db)
        #entity_to_database.add_standard_entity_to_attribute_table()
        entity_to_database.add_message_to_database()

    #def format(self, estring):
    #    estring

    def find_people(self,relationship):
        dbfrom = DatabaseToPerson(self.db)
        dbfrom.add_attribute_table_getter(EmailAttributeTableGetter(self.db))
        peoplelist = dbfrom.get_people_from_database()
        pid = -1
        mid = -1
        #email_list = []
        for emailmessage in self.emails: #inside IMAP, generated emailmessages
            #print 'email: '+emailmessage.people['FROM']
            flag = False #pulled from db reconstructed people (all)
            email_list=[]
            for person in peoplelist:
                for pemail in person.emails:
            #for name in emailmessage.people['FROM']: #one set of emailaddress

            # pemail.address +" name: "+name + " FROM: "
                    if pemail.address == email_format(emailmessage.people[relationship]): #if there is a person in db with an email contained in an emailmessage
                        #print email_format(emailmessage.people['FROM'])
                        pid = person.person_id
                        #print pid
                        #self.personid_list.append(pid)
                        print "Existing Contact Identified, Relationship added"+str(pid)
                        emailmsg_person(emailmessage.messageid,pid,"relationship","../../System/personal_graph.db")
                             #don't create new obj, just update DB
                        flag = True
                        break

            if (flag == False): #If email from emessage not found in people from db

                email = email_format(emailmessage.people[relationship]) #parse the email
                #print email
                #if email not in email_list:
                em = Email.Email()
                em.address= email
                print "new Email created:"+email
                #    if em not in email_list:
                #email_list.append(em) #add address to person's known addresses
                p = Person.Person()
                #p.emails=email_list
                p.emails.append(em)
                peoplelist.append(p)
                print "new Person w/email"+p.emails[0].address
                if p not in self.person_list:
                    self.person_list.append(p) #add to list of people to be pushed
                if p not in self.push_these_people_to_database:
                    self.push_these_people_to_database.append(p)
                #self.push_person_to_table(p)
                #emailmsg_person(emailmessage.messageid, p.person_id, "FROM", "../../System/personal_graph.db")

        print self.push_these_people_to_database
        p_db = PersonToDatabase(self.push_these_people_to_database, "../../System/personal_graph.db")
        email_attr = EmailAttributeTableSetter("../../System/personal_graph.db")
        p_db.add_attribute_table_setter(email_attr)
        pid_new = p_db.add_people_to_database()

        #print "People updated:"
        #print self.personid_list
        #print "People created:"
        #for p in self.person_list:
        #    print "Email of P Created"
        #    print p.emails
        #for email in email_list:
        #    print email

        #self.push_person_to_table()


    #INSERT INTO EMAIL
    def push_message_to_table(self):
        e_db = EmailMessageToDatabase(self.emails, "../../System/personal_graph.db")
        self.messageid_list = e_db.add_message_to_database()


    def push_person_to_table(self,person):
         p_db = PersonToDatabase([person], "../../System/personal_graph.db")
         email_attr = EmailAttributeTableSetter("../../System/personal_graph.db")
         p_db.add_attribute_table_setter(email_attr)
         pid_new = p_db.add_people_to_database()

def email_format(email):
    if ('>' in email):
        email = email
        email_split = email.split('<')
        email = email_split[1].rstrip('>')

    return email

def push_into_relation(emails):
    for p in emails.people:
        print 'do'



conn = IMAPConnector("../../System/personal_graph.db")
conn.run()
#conn.check_success()
conn.push_message_to_table()
for relation in ['FROM','TO','CC','BCC']:
    conn.find_people(relation)
#print conn.person_list
#print "personidlist"
#print conn.personid_list
#conn.push_person_to_table()
