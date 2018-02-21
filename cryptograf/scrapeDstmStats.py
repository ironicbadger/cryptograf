import json
import requests
import jsonrpclib
from influxdb import InfluxDBClient

def getGPUStats():
    server = jsonrpclib.Server('http://192.168.1.9:2222')
    r = server.getstat(1)

    # returns a list of dicts
    # one dict per GPU    
    return r

# pass in list of dicts from getGPUStats
def calcAverageSols(listOfGPUs):
    solAvgTotal = 0
    for dict in listOfGPUs:
        solAvgTotal = solAvgTotal + dict['avg_sol_ps']
        
    return solAvgTotal

# pass in list of dicts from getGPUStats
def calcCurrentTotalSols(listOfGPUs):
    solTotal = 0
    for dict in listOfGPUs:
        solTotal = solTotal + dict['sol_ps']
        
    return solTotal

def writeGpuStatsToInflux():
    stats = getGPUStats()

    client = InfluxDBClient('192.168.1.2', 8086, 'root', 'root', 'mining')
    client.create_database('mining')

    ## format data for InfluxDB
    for d in stats:
        json = [
            {
                "measurement": "DSTM",
                "tags": {
                    "rig": "beast",
                    "GPU_ID": d['gpu_id']
                },
                "fields": {
                    "Latency": d['latency'],
                    "Avg SOL/s per Watt": d['avg_sol_pw'],
                    "Power Usage": d['power_usage'],
                    "Temperature": d['temperature'],
                    "Avg SOL/s per Second": d['avg_sol_ps'],
                    "Avg Power Usage": d['avg_power_usage'],
                    "SOL/s": d['sol_ps']
                }
            }
        ]
        client.write_points(json)
    
    # write total SOL/s to Influx
    totalSols = calcCurrentTotalSols(stats)
    totalAvgSols = calcAverageSols(stats)
    json = [
        {
            "measurement": "DSTM",
            "tags": {
                "rig": "beast"
            },
            "fields": {
                "Total SOL/s": totalSols,
                "Total Avg SOL/s": totalAvgSols
            }
        }
    ]
    client.write_points(json)
