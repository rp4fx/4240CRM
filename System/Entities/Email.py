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
        self.addressfrom=[]
        self.addressto=[]
        self.addresscc=[]
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
                print 'message wrapped'
                maintype = msg.get_content_maintype()
                if maintype == 'multipart':
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            self.textbody= part.get_payload()
                elif maintype == 'text':
                    self.textbody= msg.get_payload()

                self.subject=msg['SUBJECT']
                self.addressfrom=msg['FROM']
                self.addressto=msg['TO']
                self.addresscc=msg['CC']
                self.timestamp=msg['DATE']
                #print "To:"+self.addressto+" From:"+self.addressfrom+" Subject:"+self.subject+ "Body:"+self.textbody
               # elif:


