__author__ = 'roran_000'

from Tkinter import *
from Tkinter import Message as TkMessage
from ttk import *
#from PIL import Image, ImageTk
from functools import partial
from System.DatabaseToEntity import *
import datetime
import time


def get_time_from_timestamp(unix_time):
    if unix_time is 0:
        str_time = ""
    else:
        str_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')
    return str_time

def get_timestamp_from_time(str_time):
    if str_time is "":
        return 0
    else:
        time_object = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        return time.mktime(time_object)


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
        columns = ('First Name', 'Last Name', 'Gender', 'Birthday', "Last Interaction")
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
        if col == "First Name":
            FirstNameTreeSortStrategy().sort(self.tree, "name")
        elif col == "Last Name":
            LastNameTreeSortStrategy().sort(self.tree, "name")
        elif col == "Gender":
            GenderTreeSortStrategy().sort(self.tree, "gender")
        elif col == "Birthday":
            print "Birthday sorting is not currently supported."
            #BirthdayTreeSortStrategy().sort(self.tree, "birthday")
        elif col == "Last Interaction":
            LastInteractionTreeSortStrategy().sort(self.tree, "last_interaction")

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
        PersonPopUp(person, self.messages)

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
            self.set_last_interaction(person)
            last_interaction_pretty = get_time_from_timestamp(int(person.relationships["LAST_INTERACTION"]))
            try:
                #tree.insert('', 'end', str(person.person_id), text=str(person.person_id), tags=('#person'), values=(str(person.first_name) + " " + str(person.last_name) + " " + str(person.gender) + " " + str(person.birthday)))
                tree.insert('', 'end', str(person.person_id), text=str(person.person_id), tags=('#person'), values=(str(person.first_name), str(person.last_name), str(person.gender), str(person.birthday), last_interaction_pretty))
                print "Person ID: " + str(person.person_id)
                print "First Name: " + str(person.first_name)
                print "Last Name: " + str(person.last_name)
                print "Gender: " + str(person.gender)
                print "Birthday: " + str(person.birthday)
                print "Last Interaction: " + str(person.relationships["LAST_INTERACTION"])
            except Exception,e:
                print str(e)
            index += 1

    def set_last_interaction(self, person):
        last_interaction = 0
        for relationship in ["TO", "FROM", "CC", "BCC"]:
            try:
                for message in person.relationships[relationship]:
                    if message.timestamp > last_interaction:
                        last_interaction = message.timestamp
            except:
                print "No relationship %s" %(relationship)
        person.relationships["LAST_INTERACTION"] = last_interaction

    def maximize(self):
        sw = self.parent.winfo_screenwidth()-100
        sh = self.parent.winfo_screenheight()-100
        w = sw
        h = sh
        self.parent.geometry('%dx%d+%d+%d' % (w, h, 0, 0))

    def add_quit_button(self):
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=50, y=50)


class PersonPopUp:
    def __init__(self, person, messages):
        self.top_level = Toplevel(height="1000", width="1000")
        self.person = person
        self.messages = messages
        self.init_pop_up()

    def init_pop_up(self):
        user_details_paned_window = self.create_person_details_paned_window(self.top_level)
        user_details_frame = self.create_person_details_frame(user_details_paned_window)
        self.add_person_details(user_details_frame)
        self.add_notes_to_paned_window(user_details_paned_window, self.person)
        self.add_messages(self.person)

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

    def add_person_details(self, user_details_frame):
        self.add_profile_image(user_details_frame)
        self.add_name(user_details_frame)
        self.add_other_name(user_details_frame)
        self.add_birthday(user_details_frame)
        self.add_gender(user_details_frame)
        self.add_emails(user_details_frame)
        self.add_phones(user_details_frame)

    def add_profile_image(self, user_details_frame):
        img_file = "user-icon.gif"
        img = PhotoImage(file=img_file, width=100, height=100)
        image_label = Label(user_details_frame, image=img)
        image_label.grid(row=0, column=0, rowspan=7)
        image_label.image = img

    def add_name(self, user_details_frame):
        name_label = Label(user_details_frame, text=str(self.person.first_name) + " " + str(self.person.last_name))
        name_label.grid(row=0, column=2, columnspan=2, sticky=W+E)

    def add_other_name(self, user_details_frame):
        other_name_label = Label(user_details_frame, text=str(self.person.other_name))
        other_name_label.grid(row=1, column=2, columnspan=2, sticky=W+E)

    def add_birthday(self, user_details_frame):
        birthday_label = Label(user_details_frame, text="Birthday:")
        birthday_label.grid(row=3, column=2, sticky=W+E)
        actual_birthday_label = Label(user_details_frame, text=str(self.person.birthday))
        actual_birthday_label.grid(row=3, column=3, sticky=W+E)

    def add_gender(self, user_details_frame):
        gender_label = Label(user_details_frame, text="Gender:")
        gender_label.grid(row=4, column=2, sticky=W+E)
        actual_gender_label = Label(user_details_frame, text=str(self.person.gender))
        actual_gender_label.grid(row=4, column=3, sticky=W+E)

    def add_emails(self, user_details_frame):
        email_label = Label(user_details_frame, text="Emails:")
        email_label.grid(row=5, column=2, sticky=W+E+N)
        actual_email_label = Label(user_details_frame)
        actual_email_label.grid(row=5, column=3, sticky=W+E)
        for email in self.person.emails:
            temp_email_label = Label(actual_email_label, text=str(email.address), anchor=E)
            temp_email_label.config(anchor=E)
            temp_email_label.pack()

    def add_phones(self, user_details_frame):
        phone_label = Label(user_details_frame, text="Phones:")
        phone_label.grid(row=6, column=2, sticky=W+E+N)
        actual_phone_label = Label(user_details_frame)
        actual_phone_label.grid(row=6, column=3, sticky=W+E)
        for phone in self.person.phones:
            temp_phone_label = Label(actual_phone_label, text=str(phone.type) + " - " + str(phone.number), anchor=E)
            temp_phone_label.config(anchor=E)
            temp_phone_label.pack()

    def add_notes_to_paned_window(self, user_details_paned_window, person):
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

    def add_messages(self, person):
        messages_frame = Frame(self.top_level)
        messages_frame.pack(fill=BOTH, expand=1)
        self.message_tree = self.create_message_tree(messages_frame)
        self.add_messages_to_tree(person, self.message_tree)
        self.message_tree.bind("<<TreeviewSelect>>", self.message_tree_message_click_handler)

    def create_message_tree(self, message_frame):
        columns = ('Source', 'Subject', 'Date')
        message_tree = Treeview(message_frame, columns=columns)
        message_tree.pack(fill=BOTH, expand=1)
        message_tree.column('#0', width=15)
        self.add_click_handlers_to_tree_column_headers(message_tree, columns, self.message_tree_header_click_handler)
        #self.add_scrollbars(message_tree)
        return message_tree

    def add_click_handlers_to_tree_column_headers(self, tree, columns, click_handler):
        for col in columns:
            tree.heading(col, text=col, command=partial(click_handler, col))

    def add_messages_to_tree(self, person, message_tree):
        messages_tree_has_messages = False
        for relationship in ["TO", "FROM", "CC", "BCC"]:
            if relationship in person.relationships.keys():
                for message in person.relationships[relationship]:
                    messages_tree_has_messages = True
                    pretty_date = get_time_from_timestamp(message.timestamp) 
                    message_tree.insert('', 'end', str(message.messageid), text=str(message.messageid), tags=('#message'), values=("message.source", str(message.subject), pretty_date))
                    #temp_message_label = Label(messages_frame, text=str(message.subject))
                    #temp_message_label.pack(fill=BOTH)

        if not messages_tree_has_messages:
            message_tree.insert('', 'end', "-1", text="no messages", tags=('#no_messages'), values=("", "No messages available", ""))

    def message_tree_header_click_handler(self, event):
        print "Clicked a message tree header!"

    def message_tree_message_click_handler(self, event):
        print "Clicked a message!"
        message_id = str(self.message_tree.focus())
        if message_id is not "no messages":
            message = self.get_message_by_id(message_id)
            self.create_message_popup(message)
            print str(self.message_tree.focus())

    def get_message_by_id(self, message_id):
        print "searching for message with message id: %s" % message_id
        for m in self.messages:
            if str(m.messageid) == message_id:
                print "Found message :)"
                return m
        print "Did not find message :("
        return Message("", "", "")

    def create_message_popup(self, message):
        MessagePopUp(message)


class MessagePopUp:
    def __init__(self, message):
        self.top_level = Toplevel(height="1000", width="1000")
        self.message = message
        self.init_pop_up()

    def init_pop_up(self):
        message_details_frame = self.create_message_details_frame(self.top_level)
        self.add_message_header(message_details_frame)
        self.add_subject(message_details_frame)
        self.add_message_content(message_details_frame)

    def create_message_details_frame(self, parent):
        message_details_frame = Frame(parent, borderwidth=5)
        message_details_frame.pack(fill=BOTH, expand=1)
        self.configure_columns(message_details_frame)
        self.configure_rows(message_details_frame)
        return message_details_frame

    def configure_columns(self, message_details_frame):
        message_details_frame.columnconfigure(0, pad=3)
        message_details_frame.columnconfigure(1, pad=3)
        message_details_frame.columnconfigure(2, pad=3)
        message_details_frame.columnconfigure(4, pad=3)
        message_details_frame.columnconfigure(5, pad=3)
        message_details_frame.columnconfigure(6, pad=3)

    def configure_rows(self, message_details_frame):
        message_details_frame.rowconfigure(0, pad=3)
        message_details_frame.rowconfigure(1, pad=3)
        message_details_frame.rowconfigure(2, pad=3)
        message_details_frame.rowconfigure(3, pad=3)
        message_details_frame.rowconfigure(4, pad=3)
        message_details_frame.rowconfigure(5, pad=3)
        #message_details_frame.rowconfigure(6, pad=3)

    def add_message_header(self, message_details_frame):
        self.add_from(message_details_frame)
        self.add_to(message_details_frame)
        self.add_cc(message_details_frame)
        self.add_bcc(message_details_frame)

    def add_from(self, message_details_frame):
        from_label = Label(message_details_frame, text="From:")
        from_label.grid(row=0, column=0, sticky=W+E)
        if len(self.message.people["FROM"]) > 0:
            actual_to_label= Label(message_details_frame, text=str(self.format_person(self.message.people["FROM"][0])))
        else:
            actual_to_label= Label(message_details_frame, text="")
        actual_to_label.grid(row=0, column=1, sticky=W+E)

    def add_to(self, message_details_frame):
        to_label = Label(message_details_frame, text="To:")
        to_label.grid(row=1, column=0, sticky=W+E)
        actual_to_label = Label(message_details_frame)
        actual_to_label.grid(row=1, column=1, sticky=W+E)
        for person in self.message.people["TO"]:
            temp_to_label = Label(actual_to_label, text=str(self.format_person(person)), anchor=E)
            temp_to_label.config(anchor=E)
            temp_to_label.pack()

    def add_cc(self, message_details_frame):
        cc_label = Label(message_details_frame, text="CC:")
        cc_label.grid(row=2, column=0, sticky=W+E)
        actual_cc_label = Label(message_details_frame)
        actual_cc_label.grid(row=2, column=1, sticky=W+E)
        for person in self.message.people["CC"]:
            temp_label = Label(actual_cc_label, text=str(self.format_person(person)), anchor=E)
            temp_label.config(anchor=E)
            temp_label.pack()

    def add_bcc(self, message_details_frame):
        bcc_label = Label(message_details_frame, text="BCC:")
        bcc_label.grid(row=3, column=0, sticky=W+E)
        actual_bcc_label = Label(message_details_frame)
        actual_bcc_label.grid(row=3, column=1, sticky=W+E)
        for person in self.message.people["BCC"]:
            temp_label = Label(actual_bcc_label, text=str(self.format_person(person)), anchor=E)
            temp_label.config(anchor=E)
            temp_label.pack()

    def add_subject(self, message_details_frame):
        subject_label = Label(message_details_frame, text=str(self.message.subject))
        subject_label.grid(row=4, column=0, columnspan=6, sticky=W+E)

    def add_message_content(self, message_details_frame):
        content_text = Text(message_details_frame)
        content_text.insert(END, self.message.content)
        content_text.grid(row=5, column=0, columnspan=6, sticky=N+S+E+W)

    def format_person(self, person):
        return str(person.first_name) + " " + str(person.last_name)


class TreeSortStrategy:
    def sort(self, tree, sort_column):
        tree_node_ids = tree.get_children()
        tree_nodes_to_sort = self.create_tree_node_list_to_sort(tree, tree_node_ids)
        sorted_tree_nodes = self.get_sorted_tree_nodes(tree_nodes_to_sort)
        self.attach_sorted_items_to_tree(tree, sorted_tree_nodes, sort_column)

    def create_tree_node_list_to_sort(self, tree, tree_node_ids):
        return []

    def get_sorted_tree_nodes(self, tree_nodes_to_sort):
        return []

    def attach_sorted_items_to_tree(self, tree, sorted_tree_nodes, sort_column):
        blank_items = []
        for item in sorted_tree_nodes:
            if item[sort_column] is " " or item[sort_column] is "":
                blank_items.append(item)
            else:
                tree.move(item["item_id"], "", "end")
        for item in blank_items:
            tree.move(item["item_id"], "", "end")


class FirstNameTreeSortStrategy(TreeSortStrategy):
    def get_sorted_tree_nodes(self, tree_nodes_to_sort):
        return sorted(tree_nodes_to_sort, key=lambda item: item["name"])

    def create_tree_node_list_to_sort(self, tree, tree_node_ids):
        tree_nodes_to_sort = []
        for item in tree_node_ids:
            tree.detach(item)
            item_first_name = str(tree.item(item)["values"][0])
            item_last_name = str(tree.item(item)["values"][1])
            temp_dict = {}
            temp_dict["item_id"] = item
            if item_first_name is not "":
                temp_dict['name'] = item_first_name + " " + item_last_name
            else:
                temp_dict['name'] = item_first_name
            tree_nodes_to_sort.append(temp_dict)
        return tree_nodes_to_sort


class LastNameTreeSortStrategy(TreeSortStrategy):
    def get_sorted_tree_nodes(self, tree_nodes_to_sort):
        return sorted(tree_nodes_to_sort, key=lambda item: item["name"])

    def create_tree_node_list_to_sort(self, tree, tree_node_ids):
        tree_nodes_to_sort = []
        for item in tree_node_ids:
            tree.detach(item)
            item_first_name = str(tree.item(item)["values"][0])
            item_last_name = str(tree.item(item)["values"][1])
            temp_dict = {}
            temp_dict["item_id"] = item
            if item_last_name is not "":
                temp_dict['name'] = item_last_name + " " + item_first_name
            else:
                temp_dict['name'] = item_last_name
            tree_nodes_to_sort.append(temp_dict)
        return tree_nodes_to_sort


class GenderTreeSortStrategy(TreeSortStrategy):
    def get_sorted_tree_nodes(self, tree_nodes_to_sort):
        return sorted(tree_nodes_to_sort, key=lambda item: item["gender"])

    def create_tree_node_list_to_sort(self, tree, tree_node_ids):
        tree_nodes_to_sort = []
        for item in tree_node_ids:
            tree.detach(item)
            item_gender = str(tree.item(item)["values"][2])
            temp_dict = {}
            temp_dict["item_id"] = item
            temp_dict['gender'] = item_gender
            tree_nodes_to_sort.append(temp_dict)
        return tree_nodes_to_sort


class BirthdayTreeSortStrategy(TreeSortStrategy):
    def get_sorted_tree_nodes(self, tree_nodes_to_sort):
        return sorted(tree_nodes_to_sort, cmp=self.compare_birthdays)

    def compare_birthdays(self, item1, item2):
        if int(item1["birthday"]) - int(item2["birthday"]) > 0:
            return 1
        elif int(item1["birthday"]) - int(item2["birthday"]) < 0:
            return -1
        else:
            return 0

    def create_tree_node_list_to_sort(self, tree, tree_node_ids):
        tree_nodes_to_sort = []
        for item in tree_node_ids:
            tree.detach(item)
            item_birthday = str(tree.item(item)["values"][3])
            temp_dict = {}
            temp_dict["item_id"] = item
            temp_dict['birthday'] = item_birthday
            tree_nodes_to_sort.append(temp_dict)
        return tree_nodes_to_sort


class LastInteractionTreeSortStrategy(TreeSortStrategy):
    def get_sorted_tree_nodes(self, tree_nodes_to_sort):
        return sorted(tree_nodes_to_sort, cmp=self.compare_last_interaction)

    def compare_last_interaction(self, item1, item2):
        timestamp1 = get_timestamp_from_time(item1["last_interaction"])
        timestamp2 = get_timestamp_from_time(item2["last_interaction"])
        if timestamp1 - timestamp2 < 0:
            return 1
        elif timestamp1 - timestamp2 > 0:
            return -1
        else:
            return 0

    def create_tree_node_list_to_sort(self, tree, tree_node_ids):
        tree_nodes_to_sort = []
        for item in tree_node_ids:
            tree.detach(item)
            item_last_interaction = str(tree.item(item)["values"][4])
            temp_dict = {}
            temp_dict["item_id"] = item
            temp_dict['last_interaction'] = item_last_interaction
            tree_nodes_to_sort.append(temp_dict)
        return tree_nodes_to_sort


def main():
    print 'Loading...'
    root = Tk()
    root.geometry("1000x1000+100+100")
    app = CRM(root)
    root.mainloop()


main()
