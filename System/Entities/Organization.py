__author__ = 'roran_000'


class Organization:
    def __init__(self,orgid,name,note):
        self.orgid = orgid
        self.name = name
        self.note = note

    def __str__(self):
        return "Name: "+ self.name+ " \nNotes: "+ self.note

    def edit_name(self,name):
        self.name = name


def main():
    o = Organization(1,"hello","good")
    print o



if __name__ =="__main__":
    main()
