__author__ = 'roran_000'

from abc import *
import sqlite3 as sq


class Module():
    __metadata__ = ABCMeta
    @abstractproperty
    def db(self):pass

    @abstractproperty
    def con(self):pass

    @abstractproperty
    def cursor(self):pass

    @abstractmethod
    def get_contact_list(self):pass
        #get stuff from db

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


class msg:
    def __int__(self,MID,content,timestamp):
        self.MID = MID
        self.content = content
        self.timestamp = timestamp
    def __str__(self):
        return self.content

class person:
    def __init__(self,PID,firstname,lastname,othername,birthday,gender,note):
        self.PID = PID
        self.first = firstname
        self.last = lastname
        self.other = othername
        self.birth = birthday
        self.gender = gender
        self.note = note
    def __str__(self):
        return self.first +" "+self.last


class CRM():

    def __init__(self,curs,con,PID):
        self.curs = curs
        self.con = con
        self.PID = PID

    def contact_by_rec(self):
        self.curs.execute("SElECT * from personPerson WHERE personid = %d ORDER BY endtime"% (self.PID))
        return return_rows_db(self.curs)


    def view_contact_msg(self,con_PID,MID):
        self.curs.execute("SELECT content,timestamp FROM message NATURAL JOIN messagePerson WHERE personid = %d AND messageid = %d "%
            (con_PID,MID))
        return return_rows_db(self.curs)

    def add_msg(self,msg,con_PID,relation):
        self.curs.execute("INSERT INTO message VALUES (%d,%s,%d)"%(msg.MID,msg.content,msg.timestamp))
        self.con.commit()
        self.add_msgPerson(con_PID,msg.MID,relation)

    def add_msgPerson(self,con_PID,MID,relation):
        self.curs.execute("INSERT INTO messagePerson VALUES (%d,%d,%s)"%(MID,con_PID,relation))
        self.con.commit()


    def inc_endtime_db(self,con_PID,timestamp):
        self.curs.execute("UPDATE personPerson SET endtime = %d WHERE personid = %d AND personid = %d", (timestamp,self.PID,con_PID))
        self.con.commit()
        self.curs.execute("UPDATE personPerson SET endtime = %d WHERE personid = %d AND personid = %d", (timestamp,con_PID,self.PID))
        self.con.commit()

    def create_new_person(self,person):
        self.curs.execute("INSERT INTO person VALUES (%d,%s,%s,%s,%d,%s,%s)",
                          (person.PID,person.first,person.last,person.other,person.birth,person.gender,person.note))
        self.commit()

    def create_relation(self,con_PID,relation,time):
        self.curs.execute("INSERT INTO person VALUES (%d,%d,%s,%d,%d)", (self.PID,con_PID,relation,time,time))
        self.con.commit()
        self.curs.execute("INSERT INTO person VALUES (%d,%d,%s,%d,%d)", (con_PID,self.PID,relation,time,time))
        self.con.commit()

    def add_msg_existing(self,msg,con_PID,relation,timestamp):
        self.add_msg(msg.con_PID,relation)
        self.add_msgPerson(con_PID,msg.MID,relation)
        self.inc_endtime_db(con_PID,timestamp)

    def add_msg_new(self,msg,con_PID,relation,person):
        self.create_new_person(person)
        self.create_relation(person.PID,relation,msg.timestamp)
        self.add_msg(msg,person.PID,relation)
        self.add_msgPerson(person.PID,msg.MID,relation)



def printall_table(tableName,curs): #testing method to see whats in table
    curs.execute("SELECT * FROM %s ", (tableName))
    rows = curs.fetchall()
    for r in rows:
        print r
def connect_to_db(db_name):
    conn = sq.connect(db_name)
    curs = conn.cursor()
    return [conn,curs]


def main():
  #db_list = connect_to_db("personal_graph.db")
  #curs = db_list[1]
  #con = db_list[0]
  #curs.execute("SELECT * FROM personal_graph.sqlite_master WHERE type ='table' ")
  #rows = curs.fetchall()
  #for r in rows:
  #    print r
  #trying to access db ^ NOT WORKING
  print 'do something'





if __name__ == "__main()__":
    main()
