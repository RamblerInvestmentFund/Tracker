#------------Necessary Variables--------------#
import datetime as dt
import pandas as pd
symbols = ['LVMUY', 'FMS', 'GSK', 'NGG', 'AMZN', 'NLY', 'ARCH', 'BAX', 'BA', 'CELH', 'CL', 'XOM', 'GD', 'LMT', 'MDR', 'MRK', 'MU', 'NOC', 'PANW', 'PXD', 'RTN', 'SNAP', 'TSLA', 'VZ', 'WDC', 'UUP', 'VIXY', 'SHY', 'TLT', 'IAU', 'MINT']
allocations = [158, 350, 1106, 228, 8, 419, 287, 288, 70, 2358, 213, 252, 9, 5, 172, 567, 40, 77, 141, 9, 85, 100, 4, 747, 36, 494, 150, 2490, 425, 6768, 1477]
portfolio_info = pd.Series(allocations, index = symbols)
portfolio_info = portfolio_info.sort_index()
symbols = list(portfolio_info.index)
allocations = portfolio_info.values
start_date = dt.date(2019,01,01)
fund_name = "Rambler Investment Fund"
#Benchmark Index
bench_symbol = "SPY"

#RF Syntax: 6 MO, 2 YR etc.
rate = '1 YR'
#CUR, AVG
method = "AVG"

#For Quandl
api_key = ""

#Dirctory Input For Data and Reports
root_path = "/Users/zhaoyanbo/Desktop/RIF/nic 4:5:19/Portfolio-Tracker-master"

#------------Run Program----------------------#
if __name__ == '__main__':
    #import rebalance
    #rebalance.rebalance(allocations=allocations)
     # 1.) Import the module
    import report
    import data
    import performance
    #
    # # Select Functions
    end_date = dt.date.today()
    data.portfolio(symbols, allocations, start_date)
    data.benchmark(bench_symbol, start_date)
    performance.portfolio()
    r = report.rep(fname=root_path + '/Reports/Daily Report ' + str(end_date) + '.pdf',fund_name=fund_name,logo_path="/Users/zhaoyanbo/Desktop/RIF/nic 4:5:19/Portfolio-Tracker-master/Reports/rif.jpg")
    print '--------Cover-----'
    r.cover()
    print '--------Performance-----'
    r.perf()
    print '--------Metrics-----'
    r.mets()
    print '--------Divesification-----'
    r.diversification()
    r.savePDF()
    print 'I Ran'
