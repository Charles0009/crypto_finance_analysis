# ----------------------------------------------------------------------------------
# # Extracting Bitcoin Metrics from blockchain.info
# This code was run on 5 December 2018.
# ----------------------------------------------------------------------------------


import urllib.request, json
import pandas as pd

from functools import reduce

#Create dict to store metadata
MetaData = dict()

# Functions

#Extracting metadata:
def descriptor(field, data):
    MetaData[data['name']] = f'{field} - ' + data['unit'] + ' - ' + data['description']

#Extracting values:
def dataExtractor(field):
    with urllib.request.urlopen(f'https://api.blockchain.info/charts/{field}?timespan=2years&format=json&sampled=false') as url:
        data = json.loads(url.read().decode())
    data2 =  pd.DataFrame(data["values"])
    data2.columns = ['EpochDate', field]
    descriptor(field, data)
    return(data2)

# Applying Functions

print("Extract Data")
data_list = [dataExtractor(field) for field in ['market-price',                          #price
                                                'estimated-transaction-volume',          #vol
                                                'estimated-transaction-volume-usd',      #USD vol
                                                'trade-volume',                          #exchange vol
                                                'n-unique-addresses'                    #no. used addresses
                                                ]
                ]


print("Aggregate Data")
reduce(lambda left, right: pd.merge(left, right, on = 'EpochDate', how = 'left'), data_list).to_csv('blockchain_info_test.csv', index = False)

print("Store Meta Data")
with open('MetaData.txt', 'w') as file:
    file.write(str(MetaData))

