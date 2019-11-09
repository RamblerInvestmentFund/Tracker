import quandl
import datetime as dt
import calendar
import os
import pandas as pd
import sys
from main import root_path
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

#Dates
end_date = dt.date.today()
emo = end_date.month
eday = end_date.day
eyear = end_date.year
emonth = calendar.month_abbr[emo]

def portfolio(symbols, allocations, start_date):

    folders = [os.path.join(root_path, "Daily Data"), os.path.join(root_path, "Daily Data", "Portfolio"), os.path.join(root_path, "Daily Data", "Benchmark")]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    #Modify Symbols List
    # for symbol in symbols:
    #     for ch in ['^', '.', '-', '/']:
    #         if ch in symbol:
    #             symbols.remove(symbol)
    #             symbol = symbol.replace(ch, '_')
    #             symbols.append(symbol)

    # Update for Quandl
    #qsymbols = []
    #for i in range(len(symbols)):
    #    qsymbol = "WIKI/" + symbols[i].upper() + ".4"
    #    qsymbols.append(qsymbol)

    smo = start_date.month
    sday = start_date.day
    syear = start_date.year
    smonth = calendar.month_abbr[smo]

    #Portfolio Data

    port_data = pdr.get_data_yahoo(symbols, start=start_date, end=end_date)['Adj Close']
    print (port_data)
    #port_data.columns = symbols
    # except:
    #     print "Unable to download the yahoo data"
    #     pass

    #print port_data
    temp_data = port_data.iloc[:,0:len(port_data.columns)].apply(pd.to_numeric)
    for column in temp_data.columns:
        c = temp_data[column]
        if c.isnull().all():
            print ('WARNING:  The following symbol: '+str(column)+' has no timeseries data. This could be due to an invalid ticker, or an entry not supported by Quandl. \n You will not be able to proceed with any function in the script until all of the symbols provided are downloaded.')
            sys.exit()
    print (len(port_data))
    #print port_data
    print (port_data.columns.values)
    print (list(set(port_data.columns.values) - set(symbols)))
    port_val = port_data * allocations
    # Remove Rows With No Values

    #FIX!!!!!!
    #port_data.dropna(axis=0, how='any')
    port_val = port_val.fillna(port_val.mean())

    port_val['Portfolio Value'] = port_val.sum(axis=1)
    #print port_val

    # Calculate Portfolio Returns
    port_rets = port_val.pct_change()
    port_rets = port_rets.dropna(how='any')

    #Calculate Portfolio Weights
    assets = port_val.tail(1)
    s = port_val.iloc[-1:, -1]
    port_weights = assets / int(s)
    port_weights = port_weights.transpose()
    port_weights.columns = ["Weight"]
    port_weights = port_weights.drop(port_weights.index[len(port_weights) - 1])


    port_val.to_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv"),index=True)
    port_rets.to_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv") ,index=True)
    port_data.to_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Daily_Prices.csv") ,index=True)
    port_weights.to_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Weights.csv") ,index=True)

    print ('Portfolio data has successfully been downloaded.')
def benchmark(bench_symbols, bench_allocations, start_date):

    #quandl.ApiConfig.api_key = api_key

    folders = [os.path.join(root_path, "Daily Data"), os.path.join(root_path, "Daily Data", "Benchmark"), os.path.join(root_path, "Daily Data", "Portfolio")]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
            
    smo = start_date.month
    sday = start_date.day
    syear = start_date.year
    smonth = calendar.month_abbr[smo]

    #Benchmark Data
    #bench_data = pd.read_csv(
    #    'http://finance.google.com/finance/historical?q='+str(bench_symbol)+'&startdate='+ str(smonth) +'+'+ str(sday) +'+'+ str(syear) +'&enddate='+ str(emonth) +'+'+ str(eday) +'+'+ str(eyear) +'&output=csv',
    #    index_col=0)["Close"]
    bench_data = pdr.get_data_yahoo(bench_symbols, start_date, end_date)["Adj Close"]
    bench_data.index = pd.to_datetime(bench_data.index)
    print (bench_data)
    bench_val = bench_data * bench_allocations

    bench_val = bench_val.fillna(bench_val.mean())

    bench_val['Benchmark Value'] = bench_val.sum(axis=1)

    # Calculate Benchmark Returns
    bench_rets = bench_val.pct_change()
    bench_rets = bench_rets.dropna(how='any')

    #Reverse Frame
    #bench_rets = bench_data.iloc[:: -1]
    #bench_rets = bench_rets.dropna(how='any')

    #bench_rets = bench_rets.pct_change()

    
    bench_data.to_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Price Data.csv") ,index=True)
    bench_rets.to_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Returns.csv") ,index=True)
    bench_val.to_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Value.csv") ,index=True)
    
    print ('Benchmark data has finished downloading.')
# symbols = ['LVMUY', 'FMS', 'GSK', 'NGG', 'AMZN', 'NLY', 'ARCH', 'BAX', 'BA', 'CELH', 'CL', 'XOM', 'GD', 'LMT', 'MDR', 'MRK', 'MU', 'NOC', 'PANW', 'PXD', 'RTN', 'SNAP', 'TSLA', 'VZ', 'WDC', 'UUP', 'VIXY', 'SHY', 'TLT', 'IAU', 'MINT']
# allocations = [158, 250, 1106, 228, 8, 419, 287, 288, 70, 2358, 213, 252, 9, 5, 172, 567, 40, 77, 141, 9, 85, 100, 4, 747, 36, 494, 150, 2490, 425, 6768, 148070]
# portfolio_info = pd.Series(allocations, index = symbols)
# portfolio_info = portfolio_info.sort_index()
# symbols = list(portfolio_info.index)
# allocations = portfolio_info.values
# start_date = dt.date(2019,01,01)
# print symbols
# print allocations
# print portfolio(symbols, allocations, start_date)
