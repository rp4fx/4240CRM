__author__ = 'roran_000'

from Tkinter import *
from ttk import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from functools import partial


class CRM(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
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
        #self.tree.heading('First Name', text='First Name')
        #self.tree.heading('Last Name', text='Last Name')
        #self.tree.heading('Gender', text='Gender')
        #self.tree.heading('Birthday', text='Birthday')
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
        tree.config(yscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=tree.xview)

    def item_clicked(self, event):
        item_id = str(self.tree.focus())
        item = self.tree.item(item_id)
        print str(self.tree.focus())

    def add_data_to_tree(self, tree):
        tree.insert('', 'end', 'timur', text='1', tags=('#entry'), values=('Timur Aleshin M 10/01/1991'))
        tree.insert('', 'end', 'zack', text='2', tags=('#entry'), values=('Zack Seid M'))
        tree.insert('', 'end', 'alex', text='3', tags=('#entry'), values=('Alex Harasty M'))
        tree.bind("<<TreeviewSelect>>", self.item_clicked)

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