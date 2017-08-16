import requests
import urllib2
import urllib
import time
import hmac
import hashlib
import json

initialInvestment = 20 #USD

k = open('key.txt','r')
s = open('secret.txt','r')
key = k.read()
secret = s.read()
k.close()
s.close()

def toUSD(coins):
    priceDict = {}
    url = 'https://min-api.cryptocompare.com/data/price'
    for coin in coins:
        params = {
            'fsym':coin,
            'tsyms':'USD'
        }
        r = requests.get(url=url,params=params)
        data = json.loads(r.text)
        priceDict[coin] = data['USD']
        #print(data['USD'])
    return priceDict
            
def sendCommand(command):
    req = {}
    req['command'] = command
    req['nonce'] = int(time.time()*1000)
    post_data = urllib.urlencode(req)

    sign = hmac.new(secret,post_data,hashlib.sha512).hexdigest()
    headers = {
        'Sign':sign,
        'Key':key
    }
    ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi',post_data,headers))
    jsonRet = json.loads(ret.read())
    return jsonRet

coinDict = {}
balanceDict = sendCommand('returnCompleteBalances')
for coin in balanceDict:
    if(float(balanceDict[coin]['available']) > 0):
        coinDict[coin] = float(balanceDict[coin]['available'])
        #coinList[coin+'amount'] = balanceDict[coin][

priceDict = toUSD(coinDict)
currentValue = 0
for coin in coinDict:
    value = coinDict[coin]*priceDict[coin]
    currentValue += value
print(coinDict)
print(priceDict)

print("Initial Value of portfolio in USD: "+str(initialInvestment))
print("current value of portfolio in USD: "+str(currentValue))
print("percent change from initial investment: "+str(((currentValue/initialInvestment)-1)*100))
