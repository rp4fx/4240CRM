__author__ = 'roran_000'


import sqlite3 as sq







def main():
    con = sq.connect('crm.db')
    curs = con.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS userCred (name TEXT,first TEXT,last TEXT, username TEXT,email TEXT,fb TEXT)""")
    #assume that organizations don't have first and last names so are easier to distinguish from individuals
    curs.execute("""CREATE TABLE IF NOT EXISTS emailCon (username TEXT,conEmail TEXT)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS fbCon (username TEXT,friend TEXT)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS emailMsg (conEmail TEXT,content TEXT, date TEXT,id TEXT)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS fbMsg (friend TEXT,content TEXT,date TEXT,id TEXT)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS password (username TEXT,ePass TEXT,fbPass TEXT)""")




if __name__=="__main__":
    main()


