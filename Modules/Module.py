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

def return_rows_db(self,curs):
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


class CRM():

    def __init__(self,curs,con,PID):
        self.curs = curs
        self.con = con
        self.PID = PID

    def contact_by_rec(self):
        self.curs.execute("SElECT * from personPerson WHERE personid = %d ORDER BY endtime", (self.PID))
        return return_rows_db(self.curs)


    def view_contact_msg(self,con_PID,MID):
        self.curs.execute("SELECT content,timestamp FROM message NATURAL JOIN messagePerson WHERE personId = %d AND messageId = %d ",
            (con_PID,MID))
        return return_rows_db(self.curs)

    def add_msg(self,msg):
        self.curs.execute("INSERT INTO message VALUES (msg.MID,msg.content,msg.timestamp)")
        self.con.commit()

    def add_msgPerson(self,conPID,MID):
        print 'do stuff'



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
