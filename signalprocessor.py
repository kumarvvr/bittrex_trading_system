import json
import os
from models import Trade, Message
import datetime

curdir = os.path.dirname(os.path.realpath(__file__))
currenciesfilename = "bittrexcurrencies.json"

currencies = None
with open(os.path.join(curdir,currenciesfilename)) as jsonfile:
    currencies = json.load(jsonfile)


currency_tokens = []
for currency in currencies['result']:
    currency_tokens.append('('+currency['Currency']+')')


signals_to_avoid = [
    'not a trade suggestion',
    'sell',
    'avoid',
]

positive_signals = [
    '[FIRST]',
    '[BUY]',
]




def ProcessMessage(message):
    # First check for signals to avoid
    content = message.content
    result = None

    quit = False
    for nsignal in signals_to_avoid:
        if nsignal in message.content:
            quit = True
            break

    if(quit):
        return None

    # If signals to avoid are not found, then continue search for
    # positive signals

    trades = []
    for currency in currency_tokens:
        if currency in content:
            trades.append(currency[1:len(currency)-1])

    result = []
    if len(trades) > 0:
        for trade in trades:
            result.append(Trade(trade,message.created_date))

    return result


if __name__ == '__main__':
    m = Message('[FIRST] (TKN)')
    m.SetCreatedDate(datetime.datetime.now())
    r = ProcessMessage(m)
    [print(re) for re in r]


