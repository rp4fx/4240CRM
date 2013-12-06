__author__ = 'roran_000'



class Message:
    def __init__(self,messageid,content,timestamp):
        self.messageid = messageid
        self.content = content
        self.subject = ''
        self.timestamp = timestamp #Mon, 2 Dec 2013 23:22:23 -0500
        self.people = {"TO": [], "FROM": [], "CC": [], "BCC": []} #Storing person object


    def __str__(self):
        return "Message content: "+ self.content+"\nSent: "+self.timestamp

    #@people == to, from, cc/bcc
    def set_people(self, information):
        self.people["TO"] = information["TO"]
        self.people["FROM"] = information["FROM"]
        self.people["CC"] = information["CC"]
        self.people["BCC"] = information["BCC"]

    def print_out(self):
        print self.people