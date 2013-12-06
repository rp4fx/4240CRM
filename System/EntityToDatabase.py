__author__ = 'Timur'
import sqlite3


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
class EmailToDatabase(EntityToDatabase):
    def add_standard_entity_to_attribute_table(self):
        phone_processor = PhoneAttributeTableSetter(self.db)
        self.add_attribute_table_setter(phone_processor)
        email_processor = EmailAttributeTableSetter(self.db)
        self.add_attribute_table_setter(email_processor)

    def add_people_to_database(self):
        self.connect_to_database()
        print 'entity'
        print self.entities
        print 'entity end'
        for person in self.entities:
            personid = self.insert_person(person)
            print "Inserted person with id %s" %(personid)
            for entity_to_attribute_table in self.add_attribute_table_setter:
                entity_to_attribute_table.add_to_table(person, personid, self.cursor)
        self.close_db_connection()

    def insert_person(self, person):
        query = 'INSERT INTO person (firstname, lastname, othername, birthday, gender, note) ' \
                'VALUES (?, ?, ?, ?, ?, ?)'
        try:
            self.cursor.execute(query, (person.first_name,
                                        person.last_name,
                                        person.other_name,
                                        person.birthday,
                                        person.gender,
                                        person.note))
            return self.cursor.lastrowid
        except:
            return -1

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
            print "Inserted person with id %s" %(personid)
            for attribute_table_setter in self.attribute_table_setters:
                attribute_table_setter.add_to_table(person, personid, self.cursor)
        self.close_db_connection()
        return self.personid_list

    def insert_person(self, person):
        query = 'INSERT INTO person (firstname, lastname, othername, birthday, gender, note) ' \
                'VALUES (?, ?, ?, ?, ?, ?)'
        try:
            self.cursor.execute(query, (person.first_name,
                                        person.last_name,
                                        person.other_name,
                                        person.birthday,
                                        person.gender,
                                        person.note))
            return self.cursor.lastrowid
        except:
            return -1


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
        try:
            self.cursor.execute(query, (personid, email.address))

            return self.cursor.lastrowid

        except:
            return -1