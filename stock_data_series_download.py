# %%

###importing stuff
import yahoo_fin
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
import pandas as pd
import yfinance as yf
import traceback
import numpy as np
import os
import glob
pd.set_option('display.max_rows', 10000)

# %%

# defining stock index and importing stocks

index_choice = 'nasdaq'
stock_list = si.tickers_nasdaq()
#print (stock_list)

# %%

### getting data series from Yahoo Finance

all_stock_dict = {}
for stock in stock_list:
    try:
      stock_daily = get_data(stock, start_date="01/01/2019", end_date="10/01/2020", index_as_date = True, interval="1d")
      all_stock_dict[stock]=stock_daily
    except Exception as e:
        print (repr(e))
    else:
        print (stock_daily)

print (all_stock_dict)

# %%

### exporting data series to CSVs

for stock_key, stock_value in all_stock_dict.items():
  date_range = f"{str(stock_value.index[0])[:-9]}_{str(stock_value.index[-1])[:-9]}"
  filename = f"{stock_key}_{date_range}.csv"
  full_filename = os.path.join (f'output\{index_choice}\data_series', filename)
  print(full_filename)
  stock_value.to_csv(full_filename, index=True)
  
# %%
### merging all stock CSVs into one dataframe

path = f'output\{index_choice}\download' 
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

stock_frame = pd.concat(li, axis=0, ignore_index=True)


# %%

# rename first column in df

def rename(col):
    if col.startswith("Unnamed: "):
        return "date"
    else:
        return col

stock_frame.columns = [rename(col) for col in stock_frame.columns]

stock_frame.head()

# %%
stock_frame.to_csv('output\sp500\download\sp500_allstock.csv', index = False)
#%%
stock_frame.info()
# %%
