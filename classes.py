class item:
    def __init__(self, user, URL):
        self.user = user
        self.URL = URL
        self.price = None

    def setPrice(self, p):
        self.price = p

    def getUser(self):
        return self.user

    def getURL(self):
        return self.URL

    def getPrice(self):
        return self.price

    def jdefault(o):
        return o.__dict__
