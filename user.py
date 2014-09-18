class User():

    # def __init__(self , username ,password , email):
    #    self.username = username
    #    self.password = password
    #    self.email = email
    #    self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % (self.username)

    @staticmethod
    def processlogin(username, password):
        if username == "nat" and password == "blah":
            return User.get(username)
        return None

    @staticmethod
    def get(username):
        u = User()
        u.username = "nat"
        return u
