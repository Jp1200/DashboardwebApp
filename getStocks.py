import requests
import datetime
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
api_key = open('alpha.txt', 'r').read()
# ts = TimeSeries(key=api_key.format(api_key), output_format='JSON')
rstocks = requests.get(
    'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&outputsize=compact&apikey=api_key')
result = rstocks.json()
result = result['Time Series (1min)']


df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])


for i, p in result.items():
    date = datetime.datetime.strptime(i, '%Y-%m-%d  %H:%M:%S')
    dataForAllTimes_row = [date, float(p['1. open']), float(p['2. high']), float(
        p['3. low']), float(p['4. close']), float(p['5. volume'])]
    df.loc[-1, :] = dataForAllTimes_row
    df.index = df.index+1
    #plt.plot(int(date), dataForAllTimes_row[3])

df = df.sort_values('date')
print(df)
# plot.show()
#print(dataForSingletime['1. open'])
#print(dataForSingletime['2. high'])
#print(dataForSingletime['3. low'])
#print(dataForSingletime['4. close'])
#print(dataForSingletime['5. volume'])
#dataForSingletime = dataForAllDays['2019-12-10']
