import json
import requests

apiKeyMPH = "insertAPIkey"
coinbaseAuthT = "insertAPIkey"

def getUserAllBalancesMPH():

    payload = {'page': 'api', 'action': 'getuserallbalances', 'api_key': apiKeyMPH}
    url = "https://miningpoolhub.com/index.php"
    r = requests.get(url, params=payload)
    jsonObject = r.json()
    userAllBalances = jsonObject['getuserallbalances']['data']
    return userAllBalances

def getCoinbaseAllSpotPrices():
    headers = {
        'authorization': "Bearer " + coinbaseAuthT,
        'content-type': "application/json",
    }

    # List of FIATs and COINs to be queried
    currencies = ['USD', 'GBP']
    coins = ['BTC', 'BCH', 'ETH', 'LTC']
    
    # dicts to store values
    prices = {}

    d = {}

    for coin in coins:
        
        # create dict with keys of BTC, LTC, etc

    
        for currency in currencies:
            coinCurr = (coin + "-" + currency)
            r = requests.get(url="https://api.coinbase.com/v2/prices/" + coinCurr + "/spot")
            j = r.json()

            nestedD = {
                'pricePair':coinCurr, 
                'amount':j['data']['amount'],
                'FIAT':j['data']['currency'],
                'base':j['data']['base']
                }
            # Add nested dict to key coinName
            d[coin] = nestedD

            prices[coinCurr] = d

        
    # for coin in prices:
    #     print (coin)
    #     for details in prices[coin]:
    #         print (details,':',prices[coin][details])

    #print("#################")
    
    return prices
