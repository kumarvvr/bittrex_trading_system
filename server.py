from selenium import webdriver
import os
from services import ProcessMessageBoard
import time
from signalprocessor import ProcessMessage
import datetime, dateutil
import db
from sys import platform as _platform
from bittrexapi import PlaceOrder, GetOrderPrice, PlacePresetOrder
from models import Trade
import json
from dateutil.relativedelta import *

print(_platform)



curdir = os.path.dirname(os.path.realpath(__file__))
configfilename = "config.json"

with open(os.path.join(curdir,configfilename)) as configjson:
    config = json.load(configjson)


TRADE_TIMEOUT = config["TRADE_TIMEOUT"]
ELAPSED_TIME_OFFSET = config['ELAPSED_TIME_OFFSET']
ORDER_RETRY_COUNT = config['ORDER_RETRY_COUNT']
RETRY_ORDER_IDLE_TIME = config['RETRY_ORDER_IDLE_TIME']


currentMB = None
prevMB = None
completedtrades = db.readFromDb()

# Server Start Time
server_start_time = datetime.datetime.now()

def isTradeTimedout(trade:Trade):
    tsecs = (datetime.datetime.now() - trade.moment).total_seconds()
    if tsecs > TRADE_TIMEOUT:
        print("Time out for Trade : " + str(trade) + " reached.")
        return True

    return False

def OrderCompleted(trade,res):
    print("########################################")
    print("Successfully placed order for ")
    print("Currency Name     : " + str(res[0]))
    print("Currency Quantity : " + str(res[1]))
    print("Currency Price    :" + str(res[2]))
    print("########################################")
    completedtrades.append(trade)
    db.saveToDb(completedtrades)

if __name__ == '__main__':
    print("Starting Discord Monitoring server")
    if _platform == "win32" or _platform == "win64":
        browser = webdriver.Chrome(executable_path=os.path.join(curdir, 'chromedriver.exe'))
    elif _platform == "darwin":
        browser = webdriver.Chrome()

    try:
        browser.get("http://discordapp.com")
    except Exception as e:
        print("Error opening Chrome Driver - "+e)
        exit()
    userinput = input("Press ENTER after you have logged into the Discord Web App")

    # After user input, start the server.
    unfulfilledtrades = []
    while(True):
        time.sleep(1)
        print("Checking for new messages -> "+str(datetime.datetime.now()))
        # Process every second.
        server_start_time = datetime.datetime.now()
        try:
            # Load html content from the browser object
            element = browser.find_elements_by_css_selector("div.messages.scroller")[0]

            # Send the captured html content for processing.
            currentMB = ProcessMessageBoard(element.get_attribute('innerHTML'))
            # Process the message board.
            mgroups = currentMB
            # Compare message board messages against already executed trades.

            # Pending trades reset every cycle
            pendingtrades = []
            for messagegroup in mgroups:
                messages = messagegroup.GetMessages()
                trades = []
                for m in messages:
                    et = (m.created_date - server_start_time).total_seconds() + ELAPSED_TIME_OFFSET
                    if(et > 0):
                        res = ProcessMessage(m)
                        if res is not None and len(res) > 0:
                            pendingtrades.extend(res)
                    else:
                        pass
            finaltrades = []
            for trade in pendingtrades:
                #Complete the trade.

                # First check in completed trades
                add = True
                for ctrade in completedtrades:
                    if ctrade.curname == trade.curname and str(ctrade.moment) == str(trade.moment):
                        #print("Ignoring trade : "+trade.curname+", "+str(trade.moment))
                        add=False

                if add:
                    finaltrades.append(trade)


            for trade in finaltrades:
                tradetime = trade.moment - server_start_time
                elapsedtime = tradetime.total_seconds() + ELAPSED_TIME_OFFSET
                if ( elapsedtime > 0 and trade.moment.date() == datetime.date.today() ):
                    print('---------------------------------------------')
                    print('Processing trade for : '+ str(trade))
                    try:
                        res = PlacePresetOrder(trade.curname)
                        ordersuccessful = False
                        if res == None:
                            # Order has failed.
                            # Perform a fixed number of times.
                            for i in range(ORDER_RETRY_COUNT):
                                # Sleep for a fixed time
                                time.sleep(RETRY_ORDER_IDLE_TIME)
                                res = PlacePresetOrder(trade.curname)
                                if(res is not None):
                                    ordersuccessful = True
                                    break
                                print("Retrying Trade : " + str(trade) + " , trial : "+str(i+1))


                            if not ordersuccessful:
                                # Could not place the order, try again.
                                print("Failed to execute order for : "+trade.curname)
                                print('---------------------------------------------')
                            else:
                                OrderCompleted(trade,res)
                        else:
                            OrderCompleted(trade,res)
                    except Exception as e:
                        print('---------------------------------------------------------')
                        print("Error in processing order : System error ->" + str(e))
                        print('---------------------------------------------------------')

            finaltrades = []
        except Exception as e:
            print(e)





"""
import hashlib
import hmac
import requests
import time

apikey = '';
apisecret = '';

def request_comkort( url, payload ):
        tosign = "&".join( [i + '=' + payload[i] for i in payload] )
        sign = hmac.new( apisecret, tosign , hashlib.sha512);
        headers = {'sign': sign.hexdigest(), 'nonce': int( time.time() ), 'apikey': apikey }
        r = requests.post(url, data=payload, headers=headers)
        return r.text

"""
