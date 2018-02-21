import json
import requests
from influxdb import InfluxDBClient

def getApiJsonFeed():

    url = "http://whattomine.com/coins.json"
    r = requests.get(url)
    json = r.json()
    return json

def writeWtmFeedToInflux():

    client = InfluxDBClient('192.168.1.2', 8086, 'root', 'root', 'whattomine')
    client.create_database('whattomine')

    j = getApiJsonFeed()
    for coin in j['coins']:
        dbFormattedJson = [
            {
                "measurement": "whattomine.com",
                "tags": {
                    "api": "whattomine.com",
                    "Coin": j['coins'][coin]['tag']
                },
                "fields": {
                    "tag": j['coins'][coin]['tag'],
                    "algorithm": j['coins'][coin]['algorithm'],
                    "block_time": str(j['coins'][coin]['block_time']),
                    "block_reward": float(j['coins'][coin]['block_reward']),
                    "block_reward24": float(j['coins'][coin]['block_reward24']),
                    "last_block": j['coins'][coin]['last_block'],
                    "difficulty": float(j['coins'][coin]['difficulty']),
                    "difficulty24": float(j['coins'][coin]['difficulty24']),
                    "nethash": j['coins'][coin]['nethash'],
                    "exchange_rate": j['coins'][coin]['exchange_rate'],
                    "exchange_rate24": j['coins'][coin]['exchange_rate24'],
                    "exchange_rate_vol": j['coins'][coin]['exchange_rate_vol'],
                    "exchange_rate_curr": j['coins'][coin]['exchange_rate_curr'],
                    "market_cap": j['coins'][coin]['market_cap'],
                    "estimated_rewards": j['coins'][coin]['estimated_rewards'],
                    "estimated_rewards24": j['coins'][coin]['estimated_rewards24'],
                    "btc_revenue": j['coins'][coin]['btc_revenue'],
                    "btc_revenue24": j['coins'][coin]['btc_revenue24'],
                    "profitability": j['coins'][coin]['profitability'],
                    "profitability24": j['coins'][coin]['profitability24'],
                    "lagging": j['coins'][coin]['lagging'],
                    "timestamp": j['coins'][coin]['timestamp']
                }
            }
        ]
        client.write_points(dbFormattedJson)
