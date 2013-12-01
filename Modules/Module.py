__author__ = 'roran_000'

from abc import *
import sqlite3


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

class CRM():
    print 'j'


def main():
     conn = sqlite3.connect('personal_graph.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM ")




if __name__ == "__main()__":
    main()
