import bs4 as bs
from main import root_path, symbols
import pandas as pd
import numpy as np
import datetime as dt
import calendar
import os
import requests
import inspect
import re
import ssl
from urllib.request import urlopen


def fundis(rate, method):
    if os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv")) and os.path.exists(
        os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Daily_Prices.csv")) \
        and os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv")) and os.path.exists(
    os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv")) \
        and os.path.exists(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Price Data.csv")) and os.path.exists(
    os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Returns.csv")) \
        and os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv")):


        method = method.lower()
        if os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv")):
            weights = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Weights.csv"), index_col=0)

            #Create dataframe for fundamentals
            columns = ["Trailing P/E","Forward P/E","PEG","Price/Book","Beta","Dividend Yield"]
            fundamental_df = pd.DataFrame(columns=columns, index=symbols[:3])

            count = 0

            #Ensure proper notation
            fsymbols = []
            for symbol in symbols:
                symbol = symbol.replace('_', '-')
                fsymbols.append(symbol)

            #Web scrape data
            for symbol in fsymbols:
                f_data = []
                url = 'https://finviz.com/quote.ashx?t=' + symbol
                r = requests.get(url)
                html = r.text

                try:
                    string = html.split('P/E</td>')[1].split('</b></td>')[0]
                    pe = re.findall("(\d+\.\d{1,3})", string)
                    fundamental_df.at[symbols[count],"Trailing P/E"] = pe[0]
                except IndexError:
                    print ('P/E not found for:' + symbol)
                    fundamental_df.at[symbols[count],"Trailing P/E"] = None


                try:
                    string = html.split('Forward P/E')[ 1].split('</span></b>')[0]
                    fpe = re.findall("(\d+\.\d{1,3})", string)
                    fundamental_df.at[symbols[count],"Forward P/E"] = fpe[0]
                except IndexError:
                    print ('Forward P/E not found for:' + symbol)
                    fundamental_df.at[symbols[count],"Forward P/E"] = None

                try:
                    string = html.split('PEG<')[1].split('</b></td>')[0]
                    peg = re.findall("(\d+\.\d{1,3})", string)
                    fundamental_df.ix[symbols[count], "PEG"] = peg[0]
                except IndexError:
                    print ('PEG not found for:' + symbol)
                    fundamental_df.ix[symbols[count], "PEG"] = None

                try:
                    string = html.split('P/B</')[1].split('</b></td>')[0]
                    pb = re.findall("(\d+\.\d{1,3})", string)
                    fundamental_df.ix[symbols[count], "Price/Book"] = pb[0]
                except IndexError:
                    print ('P/B not found for:' + symbol)
                    fundamental_df.ix[symbols[count], "Price/Book"] = None

                try:
                    string = html.split('Beta<')[1].split('</b></td>')[0]
                    beta = re.findall("(\d+\.\d{1,3})", string)
                    fundamental_df.ix[symbols[count], "Beta"] = beta[0]
                except IndexError:
                    print ('Beta not found for:' + symbol)
                    fundamental_df.ix[symbols[count], "Beta"] = None

                try:
                    string = html.split('Dividend %')[1].split('</b></td>')[0]
                    div = re.findall("(\d+\.\d{1,3}%)", string)
                    fundamental_df.ix[symbols[count], "Dividend Yield"] = str(div[0])[:-1]

                except IndexError:
                    print ('Dividend not found for:' + symbol)
                    fundamental_df.ix[symbols[count], "Dividend Yield"] = None

                count += 1


            fundis = fundamental_df.apply(pd.to_numeric)
            
            fundis["Dividend Yield"] = fundis["Dividend Yield"] / 100
            weights = weights["Weight"].tolist()
            temp = fundis.multiply(weights, axis=0)

            # Output
            weighted_metrics = temp.sum()

            call_name = inspect.stack()[1][3]

            if call_name != "mets":
                print ('\n')
                print ('----------Weighted Fundamentals-----------')
                print (weighted_metrics)

            #Save data
            weighted_metrics.to_csv(root_path + '/Daily Data/Portfolio/Portfolio Fundis.csv', index=True)
            fundis.to_csv(root_path + '/Daily Data/Portfolio/Asset Fundis.csv', index=True)

            port_rets = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv"))
            port_data = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Daily_Prices.csv"))
            port_val = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv"))
            bench_rets = pd.read_csv(root_path+'/Daily Data/Benchmark/Benchmark Returns.csv')
            bench_data = pd.read_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Price Data.csv"))
            bench_rets.columns = ['Date', 'Return']
            bench_data.columns = ['Date', 'Close']

            weighted_metrics = pd.read_csv(root_path + '/Daily Data/Portfolio/Portfolio Fundis.csv', index_col=0)

            # Get Day of month for risk free data
            end_date = dt.date.today()
            emo = end_date.month
            eday = end_date.day
            eyear = end_date.year
            emonth = calendar.month_abbr[emo]

            if method == "avg":

                userInDate = str(input("Please enter a date in the YYYY-MM-DD format: "))

                try:  # strptime throws an exception if the input doesn't match the pattern
                    rf_start_date = dt.datetime.strptime(userInDate, '%Y-%m-%d')
                except ValueError:
                    print ("Invalid Input. Please try again.")
                else:
                    isValid = True

                rfmo = rf_start_date.month
                rfday = rf_start_date.day
                rfyear = rf_start_date.year
                rfmonth = calendar.month_abbr[rfmo]

                url = 'https://www.quandl.com/api/v3/datasets/USTREASURY/YIELD.csv?api_key=37NeVhjr4KhAPxKds_jZ&start_date='+str(rfyear)+'-'+str(rfmonth)+'-'+str(rfday)+''
                handle = urlopen(url, context = ssl._create_unverified_context())
                rf_data = pd.read_csv(handle)[rate]
                rf = rf_data.mean() / 100

            else:
                end_date = dt.date(2018,1,3)
                emo = end_date.month
                eday = end_date.day
                eyear = end_date.year
                emonth = calendar.month_abbr[emo]

                rf_data = pd.read_csv(
                    'https://www.quandl.com/api/v3/datasets/USTREASURY/YIELD.csv?api_key=37NeVhjr4KhAPxKds_jZ&start_date='+str(eyear)+'-'+str(emonth)+'-'+str(eday)+'')[rate]
                rf =rf_data.iloc[0]/100

            beta = float(weighted_metrics.iloc[3])

            #YTD Return
            spy_ytd = float(bench_data.iloc[0, 1]) / float(bench_data.iloc[-1, 1]) - 1
            port_ytd = float(port_val['Portfolio Value'].iloc[-1]) / float(port_val['Portfolio Value'].iloc[0]) - 1

            # STDEV
            port_std = port_rets['Portfolio Value'].std() * np.sqrt(252)
            bench_std = float(bench_rets.std() * np.sqrt(252))

            # Treynor
            port_treynor = (port_ytd - rf) / beta
            market_treynor = (spy_ytd - rf) / 1

            # Alpha
            port_alpha = port_ytd - (rf + (spy_ytd - rf) * beta)

            # Sharpe
            sharpe_port = (port_ytd - rf) / port_std
            sharpe_spy = (spy_ytd - rf) / bench_std

            call_name = inspect.stack()[1][3]

            if call_name != "mets":
                print ('\n')
                print ('----------Risk Adjusted Metrics-----------')
                print ("Current Risk Free Rate " + rate + ": " + "{0:.2f}%".format(rf * 100))
                print ("Portfolio Raw Return: " + "{0:.2f}%".format(port_ytd * 100))
                print ("Benchmark Return: " + "{0:.2f}%".format(spy_ytd * 100))
                print ("Portfolio Volatility: " + "{0:.2f}%".format(port_std * 100))
                print ("Market Volatility: " + "{0:.2f}%".format(bench_std * 100))
                print ("Portfolio Sharpe: " + "{0:.2f}".format(sharpe_port))
                print ("Market Sharpe: " + "{0:.2f}".format(sharpe_spy))
                print ("Portfolio Treynor: " + "{0:.2f}".format(port_treynor))
                print ("Market Treynor: " + "{0:.2f}".format(market_treynor))
                print ("Portfolio Alpha: " + "{0:.2f}%".format(port_alpha * 100))

            else:
                data = [['','Volatility','Sharpe Ratio', 'Treynor Ratio','Alpha'],
                        ['Portfolio',"{0:.2f}%".format(port_std * 100),"{0:.2f}".format(sharpe_port),"{0:.2f}".format(port_treynor),"{0:.2f}%".format(port_alpha * 100)],
                        ['Benchmark',"{0:.2f}%".format(bench_std * 100),"{0:.2f}".format(sharpe_spy),"{0:.2f}".format(market_treynor),"-"]]

                return data


    else:
        print ('You have not downloaded the necessary data in order to calculated weighted fundamentals. Please run the port_data module.')

#Check if data downloaded to run functions
# clean this up

