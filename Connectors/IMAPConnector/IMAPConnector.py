__author___ = 'Zachary'
import imaplib
import time
from datetime import date,timedelta
from System.Entities import EmailMessage, Person, Phone
from Connectors.Connector import Connector
from System.Entities.EmailMessage import fillerStrategy
from System.EntityToDatabase import EmailToDatabase
from System.DatabasetoEntity import DatabaseToPerson,EmailAttributeTableGetter
from System.EntityToDatabase import *


class IMAPConnector(Connector):

    def __init__(self,db):
        self.emails = []
        self.server = self.serve()
        self.username = ''
        self.password = ''
        self.email_id=''
        self.db=db
    def serve(self):
       # try:
            return imaplib.IMAP4_SSL("imap.gmail.com",993)

    def run(self):
        print "Starting the IMAP Connector"
        #self.serve()
        self.username='cs4240crm'
        self.password='rohantimurzach'
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
        e_ids=self.search(self.emailquery())
        for id in e_ids[0].split():
            e = EmailMessage.EmailMessage()
            e.fillerStrategy.fill(self.server,id)
            e.set_message()
            self.emails.append(e)
        #feed = self.gd_client.GetContacts()
        #self.process_feed(feed, self.create_person)

    def check_success(self):
        for email in self.emails:
            print email.subject
            print email.timestamp
            print email.people
            print email.content

    def emailquery(self):
        t=date.today()-timedelta(days=90)
        t.replace(month=t.month-3)
        if(t.month<0):
            t.replace(month=12+t.month)
        searchquery ='(SINCE "{}")'.format(t.strftime("%d-%b-%Y"))
        return searchquery

    def search(self,emailquery):
        status,e_ids =self.server.search(None,emailquery)
        return e_ids

    def login(self):
        self.server.login(self.username,self.password)
        self.server.select()
        #self.gd_client.ClientLogin(username, password, self.gd_client.source)

    def add_emails_to_database(self):
        self.find_people()
        entity_to_database = EmailToDatabase(self.people, self.db)
        entity_to_database.add_standard_entity_to_attribute_table()
        entity_to_database.add_message_to_database()

    def format(self,estring):
        estring

    def find_people(self):
        dbfrom=DatabaseToPerson(self.db)
        dbfrom.add_attribute_table_getter(EmailAttributeTableGetter(self.db))
        peoplelist=dbfrom.get_people_from_database()
        pid = -1
        mid = -1
        email_list =[]
        pid_existing =[]

        person_list = []
        for emailmessage in self.emails: #inside IMAP, generated emailmessages
            #print emailmessage.people['FROM']
            flag=False
            for person in peoplelist:    #pulled from db reconstructed people (all)
                for pemail in person.emails:
                    #for name in emailmessage.people['FROM']: #one set of emailaddress

                        # pemail.address +" name: "+name + " FROM: "
                    if pemail.address in emailmessage.people['FROM']:
                        pid = person.person_id
                        pid_existing.append(pid)
                        flag=True
                        break
                if(flag == False):
                    email = email_format(emailmessage.people['FROM'])
                    email_list.append(email)
                    p = Person.Person()
                    p.emails.append(email)
                    person_list.append(p)
            p_db = PersonToDatabase(person_list, "../../System/personal_graph.db")
            email_attr = EmailAttributeTableSetter("../../System/personal_graph.db")

            p_db.add_attribute_table_setter(email_attr)

            pid_new = p_db.add_people_to_database()
        #for p in person_list:
        #    print "person "
        #    print p

        #INSERT INTO EMAIL

def email_format(email):
    if('>' in email):
        email = email
        email_split = email.split('<')
        email = email_split[1].rstrip('>')

    return email

'''
    def process_feed(self, feed, processing_method):
        ctr = 0
        while feed:
            # Process the feed
            ctr = processing_method(feed=feed, ctr=ctr)
            # Prepare for next feed iteration
            next_feed = feed.GetNextLink()
            feed = None
            if next_feed:
                feed = self.gd_client.GetContacts(uri=next_feed.href)

    def create_email(self, imapserve, ctr):
        for contact in feed.entry:
            print "Processing contact number %s..." % (ctr)
            p = Person.Person()
            get_name_strategy = GetNameFromGoogleContactsStrategy(contact)
            p.add_name_from_service(get_name_strategy)
            #no birthdays stored in google contacts
            self.add_note(contact, p)
            self.add_email_addresses(contact, p)
            self.add_phone_numbers(contact, p)
            self.people.append(p)
            ctr += 1
        return ctr

    def add_note(self, contact, p):
        if contact.content is not None:
            content = str(contact.content)
            content_text = ET.XML(content).text
            if content_text is not None:
                p.note = content_text

    def add_email_addresses(self, contact, p):
        if contact.email is not None:
            for email in contact.email:
                e = Email.Email()
                e.address = email.address
                p.emails.append(e)
                #print "Email: {0}".format(email.address)

    def add_phone_numbers(self, contact, p):
        if contact.phone_number is not None:
            for phone in contact.phone_number:
                if phone is not None:
                    my_phone = Phone.Phone()
                    if phone.label is not None:
                        my_phone.type = phone.label
                        my_phone.number = phone.text
                        #print "LABEL - {0}: {1}".format(phone.label, phone.text)
                    elif phone.rel is not None or phone.rel != "None":
                        formatted_rel = self.format_rel(phone.rel)
                        my_phone.type = formatted_rel
                        my_phone.number = phone.text
                        #print "REL - {0}: {1}".format(formatted_rel, phone.text)
                    else:
                        my_phone.number = phone.text
                        #print "Phone: {0}".format(phone.text)
                    p.phones.append(my_phone)

    def format_rel(self, rel):
        index_of_hashtag = rel.find("#") + 1
        return rel[index_of_hashtag:]

    def print_contacts(self):
        for person in self.people:
            person.print_out()
            print ""

    def add_contacts_to_db(self):
        entity_to_database = PersonToDatabase(self.people, self.db)
        entity_to_database.add_standard_entity_to_attribute_table()
        entity_to_database.add_people_to_database()
        '''
conn = IMAPConnector("../../System/personal_graph.db")
conn.run()
#conn.check_success()
conn.find_people()