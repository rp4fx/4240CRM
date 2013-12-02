__author__ = 'roran_000'


class Relationship:
    def __init__(self,relationship,start,end):
        self.relationship = relationship
        self.start = start
        self.end = end
    def __str__(self):
        return self.relationship