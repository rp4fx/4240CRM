__author__ = 'Timur'
import sqlite3


class EntityToDatabase:
    def __init__(self, entities, db):
        self.entities = entities
        self.db = db
        self.entity_to_attribute_table = []

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()

    def add_entity_to_attribute_table(self, entity_to_attribute_table):
        self.entity_to_attribute_table.append(entity_to_attribute_table)


class PersonToDatabase(EntityToDatabase):
    # cheater method so that I don't have to add the PhoneToAttributeTable and EmailToAttributeTable myself
    def add_standard_entity_to_attribute_table(self):
        phone_processor = PhoneToAttributeTable(self.db)
        self.add_entity_to_attribute_table(phone_processor)
        email_processor = EmailToAttributeTable(self.db)
        self.add_entity_to_attribute_table(email_processor)

    def add_people_to_database(self):
        self.connect_to_database()
        for person in self.entities:
            personid = self.insert_person(person)
            print "Inserted person with id %s" %(personid)
            for entity_to_attribute_table in self.entity_to_attribute_table:
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


class EntityToAttributeTable:
    def __init__(self, db):
        self.db = db
        self.opened_connection = False

    def get_ready_to_add(self, parent, parentid, cursor=None):
        self.parent = parent
        self.parentid = parentid
        self.cursor = cursor

    def add_to_table(self, parent, parentid, cursor=None):
        self.get_ready_to_add(parent, parentid, cursor)
        print "Override this method!"

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.opened_connection = True

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()


class PhoneToAttributeTable(EntityToAttributeTable):
    def add_to_table(self, person, personid, cursor=None):
        self.get_ready_to_add(person, personid, cursor)
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


class EmailToAttributeTable(EntityToAttributeTable):
    def add_to_table(self, person, personid, cursor=None):
        self.get_ready_to_add(person, personid, cursor)
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