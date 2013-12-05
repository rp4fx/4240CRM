__author__ = 'roran_000'

import sqlite3
from System.Entities.Person import *
from System.Entities.EmailMessage import *
from System.Entities.Organization import *
from System.Entities.Phone import *
from System.Entities.Profile import *
from System.Entities.Relationship import *
from System.Entities.Message import *


class DatabaseToEntity:
    def __init__(self, db):
        self.entities = []
        self.db = db
        self.attribute_table_getters = []

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()

    def add_attribute_table_getters(self, attribute_table_getter):
        self.attribute_table_getters.append(attribute_table_getter)

class DatabaseToPerson (DatabaseToEntity):
    def get_people_from_database(self):
        self.connect_to_database()
        self.query_database()
        for person in self.entities:
            personid = self.insert_person(person)
            print "Inserted person with id %s" %(personid)
            for entity_to_attribute_table in self.attribute_table_setters:
                entity_to_attribute_table.add_to_table(person, personid, self.cursor)
        self.close_db_connection()

    def query_database(self):
        self.cursor.execute("SElECT * from person")
        rows_from_db = return_rows_db(self.cursor)
        for row in rows_from_db:
            p = Person()
            p.person_id = row[0]
            p.first_name = row[1]
            p.last_name = row[2]
            p.other_name = row[3]
            p.birthday = row[4]
            p.gender = row[5]
            p.note = row[6]

        people_list =[]
        self.curs.execute("SELECT address from email where personid = %d " %(self.PID))
        email_list = return_rows_db(self.curs)
        self.curs.execute("SELECT number from phone where personid = %s" % (self.PID))
        phone_list = return_rows_db(self.curs)
        for p in people_list_unmade:
            person = Person(p[0],p[1],p[2],p[3],p[4],p[5],p[6],email_list,phone_list)
            people_list.append(person)

    def return_rows_db(self, cursor):
        ret = []
        rows = cursor.fetchall()
        for r in rows:
            ret.append(r)
        return ret

class AttributeTableGetter:
    def __init__(self, db):
        self.db = db
        self.opened_connection = False

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.opened_connection = True

    def close_db_connection(self):
        self.conn.commit()
        self.conn.close()

class PhoneAttributeTableGetter(AttributeTableGetter):
    def get_attribute(self, person, personid, cursor=None):
        self.cursor = cursor
        if self.cursor is None:
            self.connect_to_database()
        self.cursor.execute("SELECT emailid, address from email where personid = %d " %(personid))
        rows_from_db = return_rows_db(self.cursor)
        for row in rows_from_db:
            e = EmailMessage()
            e
        if self.opened_connection:
            self.close_db_connection()





def return_rows_db(curs):
    ret = []
    rows = curs.fetchall()
    for r in rows:
        ret.append(r)
    return ret

def check_person_exists(curs,PID):
    curs.execute("SELECT EXISTS(SELECT * FROM person WHERE personId = &d )"%(PID))
    check_empty = curs.fetchone()
    if (check_empty == 1):
        return True
    else:
        return False

def get_columns(curs,table):
    curs.execute("PRAGMA table_info (%s)" %(table))
    ret = []
    rows = curs.fetchall()
    for r in rows:
        ret.append(r[1])
    return ret

def check_attribute_exists(curs,table,attribute):
    attribute_list = get_columns(curs,table)
    if (attribute in attribute_list):
        return True
    else:
        False


class InfoFromDb:

     def __init__(self,curs,con,PID):
        self.curs = curs
        self.con = con
        self.PID = PID

     def get_people(self):
        self.curs.execute("SElECT * from person")
        people_list_unmade = return_rows_db(self.curs)
        people_list =[]
        self.curs.execute("SELECT address from email where personid = %d " %(self.PID))
        email_list = return_rows_db(self.curs)
        self.curs.execute("SELECT number from phone where personid = %s" % (self.PID))
        phone_list = return_rows_db(self.curs)
        for p in people_list_unmade:
            person = Person(p[0],p[1],p[2],p[3],p[4],p[5],p[6],email_list,phone_list)
            people_list.append(person)
        return people_list

     def get_contact_list(self): #by recent interaction
        self.curs.execute("SElECT * from personPerson WHERE personid = %d ORDER BY endtime"% (self.PID))
        contact_list_unmade = return_rows_db(self.curs)
        contact_list =[]
        for p in contact_list_unmade:
            self.curs.execute("SELECT address from email where personid = %d " %(p[0]))
            email_list = return_rows_db(self.curs)
            self.curs.execute("SELECT number from phone where personid = %s" % (p[0]))
            phone_list = return_rows_db(self.curs)
            person = Person(p[0],p[1],p[2],p[3],p[4],p[5],p[6],email_list,phone_list)
            contact_list.append(person)
        return  contact_list

     def get_organizations(self):
         self.curs.execute("SELECT * from org")
         org_list_unmade = return_rows_db(self.curs)
         org_list=[]
         for o in org_list_unmade:
             org_list.append(Organization(o[0],o[1],o[2]))
         return org_list

     def get_messages(self):
         self.curs.execute("SELECT * from messages")
         msg_list_unmade = return_rows_db(self.curs)
         msg_list=[]
         for m in msg_list_unmade:
             msg_list.append(Organization(m[0],m[1],m[2]))
         return msg_list

     def get_relationship(self,personid):
         self.curs.execute("SELECT relationship,starttime, endtime FROM personPerson"+
                           "personPerson WHERE personid = %d AND personid2 = %d ", (self.PID, personid))
         relation_list_unmade = return_rows_db(self.curs)
         relation_list =[]
         for r in relation_list_unmade:
             relation_list.append(Relationship(r[0],r[1],r[1]))
         return relation_list

     def get_messages_to(self,personid):
        self.curs.execute("SELECT content,timestamp,relationship,name FROM msgPerson NATURAL JOIN "+
                           "personPerson WHERE personid = %d AND personid2 = %d ", (self.PID, personid))
        relation_list_unmade = return_rows_db(self.curs)
        relation_list =[]
        for r in relation_list_unmade:
             relation_list.append(Relationship(r[0],r[1],r[1]))
        return relation_list

