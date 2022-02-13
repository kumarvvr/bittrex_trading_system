import json
import os
import requests
import datetime
import time
import hashlib
import hmac


curdir = os.path.dirname(os.path.realpath(__file__))
bconfigfile = "bittrex.config.json"

bconfigfile = os.path.join(curdir,bconfigfile)

with open(bconfigfile,'r') as file:
    bconfig = json.load(file)

apikey = bconfig['API_KEY']
apisecret = bconfig['API_SECRET']
marketprefix = bconfig['MARKET_PREFIX']

BASE_URL = bconfig['BASE_URL']
HASH_URL = bconfig['HASH_URL']
CURRENCY_RATE_URL = bconfig['CURRENCY_RATE_URL']
BTC_BUY_VAL = float(bconfig['BTC_BUY_VAL'])

def _generate_signature(data):
    global apisecret
    key = apisecret # Defined as a simple string.
    key_bytes= bytes(key , 'latin-1')
    data_bytes = bytes(data, 'latin-1') # Assumes `data` is also a string.
    return hmac.new(key_bytes, data_bytes , hashlib.sha512).hexdigest()

def PlaceOrder(currency, quantity, rate):
    global apisecret,apikey, BASE_URL
    market = marketprefix+currency

    nonce = int(time.time()) # Unix time stamp

    baseurl = BASE_URL.format( market,quantity,rate, apikey, nonce)
    print("Hash URL : " + baseurl)
    signature = _generate_signature(baseurl)
    hdrs = {'apisign': signature}

    print("Request Header : "+str(hdrs))
    print("Placing order for " + str(currency) + " for Q : " + str(quantity) + " Rate : " + str(rate))
    print("Awaiting result...")
    print("Response from Bittrex : ")
    r = requests.get(baseurl, headers=hdrs)
    r = r.json()

    print(json.dumps(r, indent=2))
    if r['success']:
        print("Trade successfully executed...")
        return r['result']['uuid']
    else:
        print("Error placing above trade")
        return None

def PlacePresetOrder(currency):
    currency_price = GetOrderPrice(currency)
    if currency_price is not None:
        # Place the order
        print(" Current Value of "+str(currency)+" is "+ str(currency_price))
        currqty = float(BTC_BUY_VAL/currency_price)
        res = PlaceOrder(currency,currqty,currency_price)
        if res is None:
            return None
        else:
            return [currency,currqty,currency_price]
    else:
        return None

def GetOrderPrice(currency):
    curr = marketprefix+currency
    url = CURRENCY_RATE_URL.format(curr)
    res = requests.get(url)
    if res.status_code == 200:
        res = res.json()
        if res['success']:
            price = res['result']['Ask']
            price = float(price)
            return price
            #print(price)
        else:
            print("Error for "+currency+" : " + res['message'])
            return None
            #print("Error")

if __name__ == '__main__':
    print(BTC_BUY_VAL)