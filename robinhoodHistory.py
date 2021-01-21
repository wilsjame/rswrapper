from dotenv import load_dotenv, find_dotenv
import os
import robin_stocks
import datetime
import numpy

"""
Turn off two-factor authentication (MFA) in your robinhood account.
Create a file named .env in the same directory as this, robinhoodHistory.py.
The two lines in .env are:
RH_USERNAME=abc@hotmail.com
RH_PASSWORD=xyz123
"""

load_dotenv(find_dotenv())
#print(os.environ['RH_USERNAME'])
#print(os.environ['RH_PASSWORD'])
login = robin_stocks.login(os.environ['RH_USERNAME'], os.environ['RH_PASSWORD'])

# Time between data points: 15second, 5minute, 10minute, hour, day, or week
INTERVAL = '10minute'
# Entire time frame to collect data points: hour, day, week, month, 3month, year, 5year
SPAN = 'week'

# historicalData is a list of dictionaries containing every key/value pair
historicalData = robin_stocks.get_crypto_historicals('BTC', interval=INTERVAL, span=SPAN, bounds='24_7', info=None)

# Extract values we're interested in
beginsAt = [data['begins_at'] for data in historicalData]
closePrice = [data['close_price'] for data in historicalData]
assert(len(beginsAt) == len(closePrice))

# Convert UTC timestamps to unix timestamps
timeStamps = [datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ").timestamp() for data in beginsAt]

print(closePrice)
print(timeStamps)

numpy.save('btcCostArray.npy', closePrice)
numpy.save('btcTimeArray.npy', timeStamps)

robin_stocks.logout()
