__author__ = 'Timur'
import System.Entities.Message
import time
import email
from datetime import date
import Message
class EmailMessage(Message.Message):
    def __init__(self):
        self.fillerStrategy=fillerFromIMAPStrategy()
        self.content = ''
        self.subject =''
        self.timestamp = '' #Mon, 2 Dec 2013 23:22:23 -0500
        self.people = {"TO": [], "FROM": [], "CC": [], "BCC": []}
    def print_out(self):
        print self.address
    def set_message(self):
        self.content = self.fillerStrategy.textbody
        self.subject = self.fillerStrategy.subject
        self.timestamp = self.fillerStrategy.timestamp #Mon, 2 Dec 2013 23:22:23 -0500
        #self.people["TO":self.fillerStrategy.addressto,"FROM":self.fillerStrategy.addressfrom,"CC":self.fillerStrategy.addresscc,"BCC":self.fillerStrategy.addressbcc]
        self.set_people(self.fillerStrategy.information)
        self.messageid =None

class fillerStrategy:
    def __init__(self):
        self.addressto=[]
        self.addressfrom=[]
        self.addresscc=[]
        self.addressbcc=[]
    def fill(self, source, identifier):
        return 1


class fillerFromIMAPStrategy(fillerStrategy):
    def fill(self, source, e_id):
        typ, msg_data = source.fetch(e_id,'(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):

                msg = email.message_from_string(response_part[1])
                maintype = msg.get_content_maintype()
                if maintype == 'multipart':
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            self.textbody= part.get_payload()
                elif maintype == 'text':
                    self.textbody= msg.get_payload()
                #works
                self.subject=msg['SUBJECT']

                if "," in msg['TO'] and msg['TO'] is not None:
                    self.addressto.append(msg['TO'].split(","))
                else:
                    self.addressto.append([msg['TO']])
                if "," in msg['FROM']and msg['FROM'] is not None:
                    self.addressfrom.append(msg['FROM'].split(","))
                else:
                    self.addressfrom.append([msg['FROM']])
                if msg['BCC'] is not None:
                    if "," in msg['BCC']:
                        self.addressbcc.append(msg['BCC'].split(","))
                    else:
                        self.addressbcc.append([msg['BCC']])
                if msg['CC'] is not None:
                    if "," in msg['CC']:
                        self.addresscc.append(msg['CC'].split(","))
                    else:
                        self.addresscc.append([msg['CC']])

                #self.addresscc=msg['CC']
                #self.addressbcc=msg['BCC']
                self.timestamp=msg['DATE']
                self.information=msg
                #print "To:"+self.addressto+" From:"+self.addressfrom+" Subject:"+self.subject+ "Body:"+self.textbody
               # elif:


