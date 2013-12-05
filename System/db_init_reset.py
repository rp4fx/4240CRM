__author__ = 'Timur'
import sqlite3

def get_all_tables(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_dictionary = c.fetchall()
    final_table_list = []
    for table_list in tables_dictionary:
        #print table_list[0]
        final_table_list.append(table_list[0])
    return final_table_list

def drop_tables(c):
    table_list = get_all_tables(c)
    for table in table_list:
        c.execute('DROP TABLE {0}'.format(table))
        print "Table {0} dropped".format(table)

def create_tables(c):
    #entity tables
    c.execute('CREATE TABLE IF NOT EXISTS person (personid INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, othername TEXT, birthday INTEGER, gender TEXT, note TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS org (orgid INTEGER PRIMARY KEY, name TEXT, note TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS message (messageid INTEGER PRIMARY KEY, content TEXT, subject TEXT, timestamp INTEGER)')
    #attribute tables
    c.execute('CREATE TABLE IF NOT EXISTS email (emailid INTEGER PRIMARY KEY, personid INTEGER, orgid INTEGER, address text)')
    c.execute('CREATE TABLE IF NOT EXISTS phone (phoneid INTEGER PRIMARY KEY, personid INTEGER, orgid INTEGER, type text, number text)')
    c.execute('CREATE TABLE IF NOT EXISTS profile (profileid INTEGER PRIMARY KEY, personid INTEGER, orgid INTEGER, username text, uri text, type text)')
    #relationship tables
    c.execute('CREATE TABLE IF NOT EXISTS personPerson (personid INTEGER, personid2 INTEGER, relationship text, starttime INTEGER, endtime INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS orgPerson (orgid INTEGER, personid INTEGER, relationship text, starttime INTEGER, endtime INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS messagePerson (messageid INTEGER, personid INTEGER, relationship text)')
    print "All tables were created."

def connect_to_db():
    conn = sqlite3.connect('personal_graph.db')
    return conn.cursor()

action = "-1"
while action == "-1":
    action = raw_input("What would you like to do (0 - initialize database; 1 - reset the database): ")
    if action == "0":
        cursor = connect_to_db()
        create_tables(cursor)
    elif action == "1":
        confirm = "-1"
        while confirm == "-1":
            print "WARNING! This action will drop all tables from the database."
            confirm = raw_input("Do you want to continue (y or n)?")
            if confirm == "y":
                cursor = connect_to_db()
                drop_tables(cursor)
            elif confirm == "n":
                print "Database was not modified."
            else:
                confirm = "-1"
                print "Unable to process your input, please try again."
    else:
        action = "-1"
        print "Unable to process your input, please try again."