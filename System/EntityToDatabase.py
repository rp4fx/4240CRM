__author__ = 'Timur'
import sqlite3
import string


class EntityToDatabase:
    def __init__(self, entities, db):
        self.entities = entities
        self.db = db
        self.attribute_table_setters = []

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()

    def add_attribute_table_setter(self, attribute_table_setter):
        self.attribute_table_setters.append(attribute_table_setter)

# RENAME THIS!!!! SHOULD BE EmailMessageToDatabase
class EmailMessageToDatabase(EntityToDatabase):


    def add_message_to_database(self):
        self.connect_to_database()
        self.messageid_list = []
        for message in self.entities:
            messageid = self.insert_message(message)
            self.messageid_list.append(messageid)
            print "Inserted message with id %s" %(messageid)

        self.close_db_connection()
        return self.messageid_list

    def insert_message(self, message):
        query = 'INSERT INTO message (messageid, content, subject,timestamp) ' \
                'VALUES (?, ?, ?, ?)'

        self.cursor.execute(query, (message.messageid,
                                        message.content,
                                        message.subject,
                                        message.timestamp))

        return self.cursor.lastrowid


class PersonToDatabase(EntityToDatabase):
    # cheater method so that I don't have to add the PhoneToAttributeTable and EmailToAttributeTable myself
    def add_standard_attribute_table_setters(self):
        phone_processor = PhoneAttributeTableSetter(self.db)
        self.add_attribute_table_setter(phone_processor)
        email_processor = EmailAttributeTableSetter(self.db)
        self.add_attribute_table_setter(email_processor)

    def add_people_to_database(self):
        self.connect_to_database()
        self.personid_list = []
        for person in self.entities:
            personid = self.insert_person(person)
            self.personid_list.append(personid)
            self.process_person(person, personid)

        #self.close_db_connection()
        return self.personid_list

    def insert_person(self, person):
        #index = self.person_in_db(person)
        #if index > 0:
        #    print "CAUGHT DUPLICATE!!!"
        #    return index
        #else:
            query = 'INSERT INTO person (firstname, lastname, othername, birthday, gender, note) ' \
                'VALUES (?, ?, ?, ?, ?, ?)'
            try:
                self.cursor.execute(query, (person.first_name,
                                        person.last_name,
                                        person.other_name,
                                        person.birthday,
                                        person.gender,
                                        person.note))
                self.conn.commit()
                return self.cursor.lastrowid
            except:
                return -1

    def person_in_db(self, person):

        query = "SELECT personid FROM person WHERE firstname='%s' AND lastname='%s' AND gender='%s'" % (person.first_name, person.last_name, person.gender)
        print
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if len(result) > 0:
                return result[0][0]
            else:
                return -1
            #print result
        except:
            print "Error in query"


    def process_person(self, person, personid):
        print "Inserted person with id %s" %(personid)
        for attribute_table_setter in self.attribute_table_setters:
            attribute_table_setter.add_to_table(person, personid, self.cursor)

    def add_person_to_database(self, person):
        self.connect_to_database()
        person_id = self.insert_person(person)
        self.process_person(person, person_id)
        self.close_db_connection()
        return person_id

class FacebookMessageToDatabase(EntityToDatabase):

    def add_to_message_table(self):
        self.connect_to_database()
        self.message_id_list = []
        for conversation in self.entities:
            for message in conversation:
                message_id = self.insert_message(message)
                self.relate_message_to_people(message, message_id)
                self.message_id_list.append(message_id)
                #self.process_message(message, message)
        self.close_db_connection()
        return self.message_id_list

    def insert_message(self, message):
        #MUST CHECK FOR ESCAPE CHARACTERS
        index = self.message_in_db(message)
        if index > 0:
            return index
        else:
            content = self.strip(message.content)
            subject = "Facebook Message"
            query = "INSERT INTO message (content, subject, timestamp) VALUES ('%s', '%s', %d)" % (content, subject, message.timestamp)
            try:
                self.cursor.execute(query)
                return self.cursor.lastrowid
            except:
                print "Weird Escape Keys Likely in Content."

    def strip(self, s):
        remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
        ret = s.translate(remove_punct_map)
        #print ret
        return ret

    def message_in_db(self, message):
        content = self.strip(message.content)
        query = "SELECT messageid FROM message WHERE content='%s' AND timestamp=%d " % (content, message.timestamp)
        print query
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if len(result) > 0:
                return result[0][0]
            else:
                return -1
            #print result
        except:
            print "Error in query"

    def relate_message_to_people(self, message, message_id):
        #preprocess for relational db
        people = message.people
        person_to_id = people["TO"][0].person_id
        person_from_id = people["FROM"][0].person_id
        query = "INSERT INTO messagePerson (messageid, personid, relationship) VALUES (%d, %d, '%s')"
        try:
            self.cursor.execute(query % (message_id, person_from_id, "from"))
            self.cursor.execute(query % (message_id, person_to_id, "to"))
        except:
            print "SQL ERROR"

class AttributeTableSetter:
    def __init__(self, db):
        self.db = db
        self.opened_connection = False

    def prepare_to_add(self, parent, parentid, cursor=None):
        self.parent = parent
        self.parentid = parentid
        self.cursor = cursor

    def add_to_table(self, parent, parentid, cursor=None):
        self.prepare_to_add(parent, parentid, cursor)
        print "Override this method!"

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.opened_connection = True

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()


class PhoneAttributeTableSetter(AttributeTableSetter):
    def add_to_table(self, person, personid, cursor=None):
        self.prepare_to_add(person, personid, cursor)
        if self.cursor is None:
            self.connect_to_database()
        for phone in self.parent.phones:
            phoneid = self.insert_phone(phone, self.parentid)
            print "Inserted phone for person %s with id %s" %(self.parentid, phoneid)
        if self.opened_connection:
            self.close_db_connection()

    def insert_phone(self, phone, personid):
        query = 'INSERT INTO phone (personid, type, number) VALUES (?, ?, ?)'
        try:
            self.cursor.execute(query, (personid, phone.type, phone.number))
            return self.cursor.lastrowid
        except:
            return -1


class EmailAttributeTableSetter(AttributeTableSetter):
    def add_to_table(self, person, personid, cursor=None):
        self.prepare_to_add(person, personid, cursor)
        if self.cursor is None:
            self.connect_to_database()
        for email in self.parent.emails:
            emailid = self.insert_email(email, self.parentid)
            print "Inserted email for person %s with id %s" %(self.parentid, emailid)
        if self.opened_connection:
            self.close_db_connection()

    def insert_email(self, email, personid):
        query = 'INSERT INTO email (personid, address) VALUES (?, ?)'

        self.cursor.execute(query, (personid, email.address))
        return self.cursor.lastrowid

class link:
    def __init__(self,entities1,entities2):
        self.entities1 =entities1
        self.entities2 = entities2
        self.db = ''

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()

class emailmsg_person(link):

    def add_msg_person(self):
        self.connect_to_database()
        for m in self.messages:
            for p in self.person:
                self.insert_into(m,p)

    def insert_into(self,message,person):
        query = 'INSERT INTO messagePerson (messageid,personid) VALUES (?,?)'
        self.cursor(query,(message.messageid,person.personid))


def emailmsg_person(messageid,personid,db):
     conn = sqlite3.connect(db)
     cursor = conn.cursor()
     cursor('INSERT INTO messagePerson (messageid,personid) VALUES (?,?)',(messageid,personid) )
     conn.commit()
     conn.close()