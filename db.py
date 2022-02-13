from models import Trade
import os
import json
import datetime

dbdir = os.path.dirname(os.path.realpath(__file__))

dbname = "completedtrades.json"

dbfile = os.path.join(dbdir,dbname)

if os.path.isfile(dbfile):
    pass
else:
    # Create an empty file.
    dbfile_ptr = open(dbfile,mode='w')

def saveToDb(trades):
    # save the list to the db.
    try:
        tdict = {}
        for t in trades:
            tdict[t.id] = [t.curname,str(t.moment)]

        with open(dbfile,'w') as fp:
            json.dump(tdict,fp)

        return True
    except Exception as e:
        print("Error writing file -" + e)
        return False

def readFromDb():
    result = []

    with open(dbfile,'r') as fp:
        try:
            data = json.load(fp)
        except Exception as e:
            data = {}

    keys = data.keys()

    for key in keys:
        value = data[key]
        currency = value[0]
        dt = datetime.datetime.strptime(value[1],'%Y-%m-%d %H:%M:%S')
        result.append(Trade(value[0],value[1],key))

    print(result)
    return result