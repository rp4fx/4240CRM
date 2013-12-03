__author__ = 'Timur'
import System.Entities.Message
import time
import email
from datetime import date
import Message
class Email(Message.Message):
    def __init__(self):
        self.textbody = ''
        #self.htmlbody=''
        self.subject=''
        self.addresses=[]
        self.timestamp=''
        self.fillerStrategy=fillerFromIMAPStrategy()
    def print_out(self):
        print self.address
class fillerStrategy:
    def fill(self, source, identifier):
        return 1
class fillerFromIMAPStrategy(fillerStrategy):
    def fill(self, source, e_id):
        typ, msg_data = source.fetch(e_id,'(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                if not msg.is_multipart():
                    self.textbody=msg.get_payload()
                    self.subject=msg['Subeject']
                    self.address=msg['From']
                    self.timestamp=msg['Date']
                    print self.timestamp
               # elif:
                #    print "multipart message"
                    #msg.walk()
                #for header in [ 'subject', 'to', 'from' ]:
                 #   print '%-8s: %s' % (header.upper(), msg[header])



       #self.htmlbody=
       #self.subject=source.fetch(e_id, '(body[header.fields (subject)])')[0][1][9:]
       #self.addresses=source.fetch(e_id,'(BODY[HEADER.FIELDS (FROM)])')
       #timestamp=source.fetch(e_id,'(INTERNALDATE)')
       #print self.textbody
        #0