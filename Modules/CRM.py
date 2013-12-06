__author__ = 'roran_000'

from Tkinter import *
from Tkinter import Message as TkMessage
from ttk import *
#from PIL import Image, ImageTk
from functools import partial
from System.DatabaseToEntity import *


class CRM(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.people = []
        self.messages = []
        self.get_people_and_messages()
        self.initUI()

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
        self.add_click_handlers_to_tree_column_headers(self.tree, columns, self.header_clicked)
        self.add_data_to_tree(self.tree)
        self.add_scrollbars_to_tree(self.tree)

    def add_click_handlers_to_tree_column_headers(self, tree, columns, click_handler):
        for col in columns:
            tree.heading(col, text=col, command=partial(click_handler, col))

    def header_clicked(self, col):
        print "Clicked on a header %s" % col

    def add_scrollbars_to_tree(self, tree):
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
        person = self.get_person_by_id(item_id)
        self.create_person_popup(person)
        print str(self.tree.focus())

    def get_person_by_id(self, person_id):
        print "searching for person with person id: %s" % person_id
        for p in self.people:
            if str(p.person_id) == person_id:
                print "Found person :)"
                return p
        print "Did not find person :("
        return Person()

    def create_person_popup(self, person):
        top = Toplevel(height="1000", width="1000")
        self.add_person_details(person, top)
        self.add_messages(person, top)

    def create_person_details_paned_window(self, parent):
        user_details_paned_window = PanedWindow(parent, orient=HORIZONTAL)
        user_details_paned_window.pack(fill=BOTH, expand=1)
        return user_details_paned_window

    def create_person_details_frame(self, paned_window):
        user_details_frame = Frame(paned_window, borderwidth=5)
        paned_window.add(user_details_frame)
        self.configure_columns(user_details_frame)
        self.configure_rows(user_details_frame)
        return user_details_frame

    def configure_columns(self, user_details_frame):
        user_details_frame.columnconfigure(0, pad=3)
        user_details_frame.columnconfigure(1, pad=3)
        user_details_frame.columnconfigure(2, pad=3)
        user_details_frame.columnconfigure(3, pad=3)
        user_details_frame.columnconfigure(4, pad=3)

    def configure_rows(self, user_details_frame):
        user_details_frame.rowconfigure(0, pad=3)
        user_details_frame.rowconfigure(1, pad=3)
        user_details_frame.rowconfigure(2, pad=3)
        user_details_frame.rowconfigure(3, pad=3)
        user_details_frame.rowconfigure(4, pad=3)
        user_details_frame.rowconfigure(5, pad=3)
        user_details_frame.rowconfigure(6, pad=3)

    def add_person_details(self, person, top_level):
        user_details_paned_window = self.create_person_details_paned_window(top_level)
        user_details_frame = self.create_person_details_frame(user_details_paned_window)

        img_file = "user-icon.gif"
        img = PhotoImage(file=img_file, width=100, height=100)
        image_label = Label(user_details_frame, image=img)
        image_label.grid(row=0, column=0, rowspan=7)
        image_label.image = img

        name_label = Label(user_details_frame, text=str(person.first_name) + " " + str(person.last_name))
        name_label.grid(row=0, column=2, columnspan=2, sticky=W+E)

        other_name_label = Label(user_details_frame, text=str(person.other_name))
        other_name_label.grid(row=1, column=2, columnspan=2, sticky=W+E)

        birthday_label = Label(user_details_frame, text="Birthday:")
        birthday_label.grid(row=3, column=2, sticky=W+E)

        actual_birthday_label = Label(user_details_frame, text=str(person.birthday))
        actual_birthday_label.grid(row=3, column=3, sticky=W+E)

        gender_label = Label(user_details_frame, text="Gender:")
        gender_label.grid(row=4, column=2, sticky=W+E)

        actual_gender_label = Label(user_details_frame, text=str(person.gender))
        actual_gender_label.grid(row=4, column=3, sticky=W+E)

        email_label = Label(user_details_frame, text="Emails:")
        email_label.grid(row=5, column=2, sticky=W+E+N)

        actual_email_label = Label(user_details_frame)
        actual_email_label.grid(row=5, column=3, sticky=W+E)

        for email in person.emails:
            temp_email_label = Label(actual_email_label, text=str(email.address), anchor=E)
            temp_email_label.config(anchor=E)
            temp_email_label.pack()

        phone_label = Label(user_details_frame, text="Phones:")
        phone_label.grid(row=6, column=2, sticky=W+E+N)

        actual_phone_label = Label(user_details_frame)
        actual_phone_label.grid(row=6, column=3, sticky=W+E)

        for phone in person.phones:
            temp_phone_label = Label(actual_phone_label, text=str(phone.type) + " - " + str(phone.number), anchor=E)
            temp_phone_label.config(anchor=E)
            temp_phone_label.pack()

        self.add_notes_to_person_details(user_details_paned_window, person)

    def add_notes_to_person_details(self, user_details_paned_window, person):
        note_frame = Frame(user_details_paned_window, height=200)
        user_details_paned_window.add(note_frame)
        #label
        note_label = Label(note_frame, text="Notes")
        note_label.pack()
        #scrollbar
        note_scrollbar = Scrollbar(note_frame)
        note_scrollbar.pack(side=RIGHT, fill=Y)
        #text
        note_text = Text(note_frame, yscrollcommand=note_scrollbar.set, height=10)
        note_text.insert(END, person.note)
        note_text.pack()
        note_scrollbar.config(command=note_text.yview)

    def add_messages(self, person, top_level):
        messages_frame = Frame(top_level)
        messages_frame.pack(fill=BOTH, expand=1)
        message_tree = self.create_message_tree(messages_frame)
        self.add_messages_to_tree(person, message_tree)
        message_tree.bind("<<TreeviewSelect>>", self.message_tree_message_click_handler)

    def create_message_tree(self, message_frame):
        columns = ('Source', 'Subject', 'Date')
        message_tree = Treeview(message_frame, columns=columns)
        message_tree.pack(fill=BOTH, expand=1)
        message_tree.column('#0', width=15)
        self.add_click_handlers_to_tree_column_headers(message_tree, columns, self.message_tree_header_click_handler)
        #self.add_scrollbars(message_tree)
        return message_tree

    def add_messages_to_tree(self, person, message_tree):
        messages_tree_has_messages = False
        for relationship in ["TO", "FROM", "CC", "BCC"]:
            if relationship in person.relationships.keys():
                for message in person.relationships[relationship]:
                    messages_tree_has_messages = True
                    message_tree.insert('', 'end', str(message.messageid), text=str(message.messageid), tags=('#message'), values=("message.source", str(message.subject), str(message.timestamp)))
                    #temp_message_label = Label(messages_frame, text=str(message.subject))
                    #temp_message_label.pack(fill=BOTH)

        if not messages_tree_has_messages:
            message_tree.insert('', 'end', "-1", text="no messages", tags=('#no_messages'), values=("", "No messages available", ""))

    def message_tree_header_click_handler(self, event):
        print "Clicked a message tree header!"

    def message_tree_message_click_handler(self, event):
        print "Clicked a message!"


    def add_data_to_tree(self, tree):
        #self.get_people_and_messages()
        self.add_people_to_tree(tree)
        #tree.insert('', 'end', 'timur', text='1', tags=('#entry'), values=('Timur Aleshin M 10/01/1991'))
        #tree.insert('', 'end', 'zack', text='2', tags=('#entry'), values=('Zack Seid M'))
        #tree.insert('', 'end', 'alex', text='3', tags=('#entry'), values=('Alex Harasty M'))
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
    root.geometry("1000x1000+100+100")
    app = CRM(root)
    root.mainloop()


main()