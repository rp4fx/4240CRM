__author__ = 'Timur'


class Phone:
    def __init__(self):
        self.number = ''
        self.type = ''

    def print_out(self):
        if self.type is not '':
            print "%s - %s" % (self.type, self.number)
        else:
            print self.number
