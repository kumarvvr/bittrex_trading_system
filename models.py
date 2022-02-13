import datetime
from utilities import randomword

class MessageElement:
    def __init__(self):
        pass

class Message(MessageElement):

    def __init__(self, content=""):
        self.content = content
        self.created_date = None

    def SetCreatedDate(self,created_date):
        self.created_date = created_date

    def GetContent(self):
        return self.content

    def GetCreatedDate(self):
        return self.created_date

    def __str__(self):
        return self.content

class Divider(MessageElement):

    def __init__(self, dt):
        # The date time object that
        # represents the divider date
        # time object.
        self.date = dt

class MessageGroup(MessageElement):

    def __init__(self, created_date_time):
        self.created_date = created_date_time
        self.messages = []
        self.username = ""

    def GetMessages(self):
        return self.messages

    def GetMessageCount(self):
        return len(self.messages)

    def AppendMessage(self, newMessage):
        self.messages.append(newMessage)

    def __str__(self):
        rep = ""
        rep += "Message Group from User - " + self.username + ", created at :"+ str(self.created_date)
        for m in self.messages:
            rep += "\n"+str(m)
        return rep

class Trade():

    def __init__(self, curname, moment, id=None):
        self.curname = curname
        self.moment = moment
        if id == None:
            self.id = randomword(5)
        else:
            self.id = id

    def GetTrade(self):
        return [self.curname, self.moment]

    def GetTradeID(self):
        return self.id

    def __str__(self):
        return self.curname + " : " + str(self.moment)

