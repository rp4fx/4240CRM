__author__ = 'Timur'
import getpass


class Connector:
    def __init__(self):
        self.username = ''
        self.password = ''

    def request_credentials(self):
        while not self.username:
            self.username = raw_input('Please enter your username: ')
        while not self.password:
            #get pass is not working properly in the IDE so I had to disable it
            #make sure to re-enable this for the demo/deployment
            #self.password = getpass.getpass()
            self.password = raw_input('Please enter your password: ')

    def print_credentials(self):
        print "Username: {0}".format(self.username)
        pass_to_print = ''
        for char in self.password:
            pass_to_print += "*"
        print "Password: {0}".format(pass_to_print)

#Testing
conn = Connector()
conn.request_credentials()
conn.print_credentials()