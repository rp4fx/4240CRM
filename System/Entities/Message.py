__author__ = 'roran_000'



class Message:
    def __init__(self,messageid,content,timestamp):
        self.messageid = messageid
        self.content = content
        self.timestamp = timestamp
        self.people = {"TO:": [], "FROM:": [], "CC:": [], "BCC:": []}

    def __str__(self):
        return "Message content: "+ self.content+"\nSent: "+self.timestamp

    #@people == to, from, cc/bcc
    def set_people(self, information):
        self.people["TO:"] = information["TO:"]
        self.people["FROM:"] = information["FROM:"]
        self.people["CC:"] = information["CC:"]
        self.people["BCC:"] = information["BCC:"]
