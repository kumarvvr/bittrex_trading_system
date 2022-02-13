from dateutil import parser
from dateutil.relativedelta import *
import random, string
import calendar


MAX_TOKENS = 5

# Message Processing terms for processing trade signals




# MO, TU, WE, TH, FR, SA, SU
def GetDateTime(text):
    reltime = None
    tokens = text.strip().split(' ')
    if len(tokens) == 1:
        # Date is in 01/11/2018
        reltime = parser.parse(text)
        return reltime

    # Extract the relevant tokens
    l = len(tokens)-1
    ampm = tokens[l]
    time = tokens[l-1]
    relativeday = tokens[l-3]
    relativedaymodifier = None


    if(l > (MAX_TOKENS-2)):
        relativedaymodifier = tokens[l-(MAX_TOKENS-1)]


    #reltime contains time and date as per current day
    if relativedaymodifier == None:
        reltime = parser.parse(time + " " + ampm)
        if relativeday == 'Yesterday':
            reltime = reltime + relativedelta(days=-1)
    else:
        reltime = parser.parse(time + " " + ampm)
        if relativedaymodifier == 'Last':
            if(relativeday == 'Monday'):
                reltime = reltime+relativedelta(weekday=MO(-1))
            if (relativeday == 'Tuesday'):
                reltime = reltime + relativedelta(weekday=TU(-1))
            if (relativeday == 'Wednesday'):
                reltime = reltime + relativedelta(weekday=WE(-1))
            if (relativeday == 'Thursday'):
                reltime = reltime + relativedelta(weekday=TH(-1))
            if (relativeday == 'Friday'):
                reltime = reltime + relativedelta(weekday=FR(-1))
            if (relativeday == 'Saturday'):
                reltime = reltime + relativedelta(weekday=SA(-1))
            if (relativeday == 'Sunday'):
                reltime = reltime + relativedelta(weekday=SU(-1))
        else:
            pass
    return reltime




def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


if __name__ == '__main__':
    print("Loading currencies")