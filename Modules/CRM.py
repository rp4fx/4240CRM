__author__ = 'roran_000'

from Tkinter import *
from ttk import *
from functools import partial
from System.DatabaseToEntity import *


class CRM(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.people = []
        self.messages = []

    def initUI(self):
        self.parent.title("Personal CRM")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.add_tree()
        self.maximize()
        #self.add_quit_button()

    def add_tree(self):
        columns = ('First Name', 'Last Name', 'Gender', 'Birthday')
        self.tree = Treeview(self, columns=columns)
        self.tree.pack(fill=BOTH, expand=1)
        self.tree.column('#0', width=10)
        for col in columns:
            #self.tree.heading(col, text=col, command=lambda: self.header_clicked(col))
            self.tree.heading(col, text=col, command=partial(self.header_clicked, col))

        self.add_data_to_tree(self.tree)

        self.add_scrollbars(self.tree)

    def header_clicked(self, col):
        print "Clicked on a header %s" % col

    def add_scrollbars(self, tree):
        y_scrollbar = Scrollbar(tree)
        y_scrollbar.pack(side=RIGHT, fill=Y)
        tree.config(yscrollcommand=y_scrollbar.set)
        y_scrollbar.config(command=tree.yview)

        x_scrollbar = Scrollbar(tree, orient=HORIZONTAL)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        tree.config(xscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=tree.xview)

    def item_clicked(self, event):
        item_id = str(self.tree.focus())
        person = self.find_person_by_id(item_id)
        self.create_person_popup(person)
        print str(self.tree.focus())

    def find_person_by_id(self, person_id):
        print "searching for person with person id: %s" % person_id
        for p in self.people:
            print p.person_id
            if str(p.person_id) == person_id:
                print "Found person :)"
                return p
        print "Did not find person :("
        return Person()

    def create_person_popup(self, person):
        top = Toplevel(height="300", width="500")
        msg = Label(top, text=str(person.first_name) + " " + str(person.last_name))
        msg.pack()

    def add_data_to_tree(self, tree):
        self.get_people_and_messages()
        self.add_people_to_tree(tree)
        tree.insert('', 'end', 'timur', text='1', tags=('#entry'), values=('Timur Aleshin M 10/01/1991'))
        tree.insert('', 'end', 'zack', text='2', tags=('#entry'), values=('Zack Seid M'))
        tree.insert('', 'end', 'alex', text='3', tags=('#entry'), values=('Alex Harasty M'))
        tree.bind("<<TreeviewSelect>>", self.item_clicked)

    def get_people_and_messages(self):
        db = "../System/personal_graph.db"
        dbToPerson = DatabaseToPerson(db)
        emailAttr = EmailAttributeTableGetter(db)
        phoneAttr = PhoneAttributeTableGetter(db)
        dbToPerson.add_attribute_table_getter(emailAttr)
        dbToPerson.add_attribute_table_getter(phoneAttr)
        self.people = dbToPerson.get_people_from_database()
        dbToMessage = DatabaseToMessage(db)
        self.messages = dbToMessage.get_messages_from_database()
        linker = PersonMessageLinker(self.people, self.messages, db)
        linker.link()

    def add_people_to_tree(self, tree):
        index = 1
        for person in self.people:
            try:
                #tree.insert('', 'end', str(person.person_id), text=str(person.person_id), tags=('#person'), values=(str(person.first_name) + " " + str(person.last_name) + " " + str(person.gender) + " " + str(person.birthday)))
                tree.insert('', 'end', str(person.person_id), text=str(person.person_id), tags=('#person'), values=(str(person.first_name), str(person.last_name), str(person.gender), str(person.birthday)))
                print "Person ID: " + str(person.person_id)
                print "First Name: " + str(person.first_name)
                print "Last Name: " + str(person.last_name)
                print "Gender: " + str(person.gender)
                print "Birthday: " + str(person.birthday)
            except Exception,e:
                print str(e)
            index += 1

    def maximize(self):
        sw = self.parent.winfo_screenwidth()-100
        sh = self.parent.winfo_screenheight()-100
        w = sw
        h = sh
        self.parent.geometry('%dx%d+%d+%d' % (w, h, 0, 0))

    def add_quit_button(self):
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=50, y=50)


def main():
    print 'do something'
    root = Tk()
    root.geometry("250x150+100+100")
    app = CRM(root)
    root.mainloop()


main()