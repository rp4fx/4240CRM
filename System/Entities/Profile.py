__author__ = 'roran_000'



class Profile:
    def __int__(self,profileid, personid, orgid, username, uri):
        self.profileid = profileid
        self.personid = personid
        self.orgid= orgid
        self.username = username
        self.uri = uri

    def __str__(self):
        return "Username: "+self.username+" \nuri: "+self.uri


    def set_username(self,username):
        self.username =username
