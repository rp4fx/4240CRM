__author__ = 'roran_000'



class Message:
    def __init__(self,messageid,content,timestamp):
        self.messageid = messageid
        self.content = content
        self.timestamp = timestamp


    def __str__(self):
        return "Message content: "+ self.content+"\nSent: "+self.timestamp

