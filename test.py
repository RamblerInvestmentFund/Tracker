#!python27
#------------Importing Packages--------------#
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override()
bench_symbol = 'SPY'
smonth = 1
sday = 1
syear = 2016
emonth = 1
eday = 1
eyear = 2018
#data = pdr.get_data_yahoo(["SPY", "IWM"], start = "2017-01-01")['Adj Close']
#print(data)
print('http://finance.google.com/finance/historical?q='+str(bench_symbol)+'&startdate='+ str(smonth) +'+'+ str(sday) +'+'+ str(syear) +'&enddate='+ str(emonth) +'+'+ str(eday) +'+'+ str(eyear) +'&output=csv')
