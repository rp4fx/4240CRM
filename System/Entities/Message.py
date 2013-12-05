__author__ = 'roran_000'



class Message:
    def __init__(self,messageid,content,timestamp):
        self.messageid = messageid
        self.content = content
        self.timestamp = timestamp
        self.people = {"to": [], "from": [], "cc": [], "bcc": []}

    def __str__(self):
        return "Message content: "+ self.content+"\nSent: "+self.timestamp

    #@people == to, from, cc/bcc
    def set_people(self, information):
        self.people["to"] = information["to"]
        self.people["from"] = information["from"]
        self.people["cc"] = information["cc"]
        self.people["bcc"] = information["bcc"]
