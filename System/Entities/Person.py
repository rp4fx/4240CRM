__author__ = 'Timur'
import xml.etree.ElementTree as ET


class Person:
    def __init__(self):
        self.person_id = ''
        self.first_name = ''
        self.last_name = ''
        self.other_name = ''
        self.birthday = -1
        self.gender = ''
        self.emails = []
        self.phones = []
        self.note = ''
        self.relationships = {}

    def add_name_from_service(self, GetNameStrategy):
        name = GetNameStrategy.get_name()
        self.first_name = name[0]
        self.last_name = name[1]
        self.other_name = name[2]

    def print_out(self):
        print "---------------------------------"
        print "First Name: %s" %(self.first_name)
        print "Last Name: %s" %(self.last_name)
        print "Other Name: %s" %(self.other_name)
        print "Birthday: %s" %(self.birthday)
        print "Gender: %s" %(self.gender)
        for email in self.emails:
            email.print_out()
        for phone in self.phones:
            phone.print_out()
        print self.note
        print "---------------------------------"

    def __str__(self):
        self.print_out()

class GetNameStrategy:
    def get_name(self):
        return ['', '', '']


class GetNameFromGoogleContactsStrategy(GetNameStrategy):
    def __init__(self, contact):
        self.contact = contact
        self.first_name = ''
        self.last_name = ''
        self.other_name = ''

    def get_name(self):
        if self.contact.name is not None:
            if self.contact.name.given_name is not None and self.contact.name.family_name is not None:
                self.first_name = ET.XML(str(self.contact.name.given_name)).text
                self.last_name = ET.XML(str(self.contact.name.family_name)).text
                #print "First: {0} | Last: {1}".format(self.first_name, self.last_name)
            elif self.contact.name.given_name is not None:
                self.first_name = ET.XML(str(self.contact.name.given_name)).text
                #print "Given Name: {0}".format(self.first_name)
            elif self.contact.name.family_name is not None:
                self.last_name = ET.XML(str(self.contact.name.family_name)).text
                #print "Family Name: {0}".format(self.last_name)
            elif self.contact.name.full_name is not None:
                self.other_name = str(self.contact.name.full_name)
                #print "Full Name: {0}".format(self.other_name)
            #else:
                #print "No name for this contact..."
        #else:
            #no name...
            #print "No name for this contact..."
        return [self.first_name, self.last_name, self.other_name]

class GetNameFromFacebookContactsStrategy(GetNameStrategy):
    #@node The json representation of GraphAPI.get(id_entity)
    def __init__(self, node):
        self.node = node
        self.first_name = ''
        self.last_name = ''
        self.other_name = ''

    def get_name(self):
        self.first_name = self.node["first_name"]
        self.last_name = self.node["last_name"]
        if "name" in self.node:
            self.other_name = self.node["name"]
        return [self.first_name,self.last_name, self.other_name]