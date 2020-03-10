import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime
#to visualize the results
import matplotlib.pyplot as plt
import seaborn
import requests_cache

import plotille

expire_after = datetime.timedelta(days=39)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
                                               
#select start date for correlation window as well as list of tickers
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 3, 4)

symbols_list = ['SPY', 'AAPL']

#array to store prices
symbols=[]

#pull price using iex for each symbol in list defined above
for ticker in symbols_list: 
    r = web.DataReader(ticker, 'yahoo', start, end, session=session)
    # add a symbol column
    r['Symbol'] = ticker 
    symbols.append(r)
    


# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
print(df.head())

df_pivot = df.pivot('Date','Symbol','Close').reset_index()
stock_table = df_pivot


def short_date(val, chars, delta, left=False):
    res = val.strftime("%x")
    return res

fig = plotille.Figure()
fig.width = 60
fig.height = 30
fig.register_label_formatter(pd._libs.tslibs.timestamps.Timestamp, short_date)

for symbol in stock_table.columns:

    if(symbol != "Date"):

        fig.plot(stock_table['Date'], stock_table[symbol], label=symbol)

print(fig.show(legend=True))

