# from pandas_datareader import data as pdr
# import datetime as dt
# end_date = dt.date.today()

# start_date = "2019-01-01"
# symbols = ['LVMUY', 'FMS', 'GSK', 'NGG', 'AMZN', 'NLY', 'ARCH', 'BAX', 'BA', 'CELH', 'CL', 'XOM', 'GD', 'LMT', 'MDR', 'MRK', 'MU', 'NOC', 'PANW', 'PXD', 'RTN', 'SNAP', 'TSLA', 'VZ', 'WDC', 'UUP', 'VIXY', 'SHY', 'TLT', 'IAU', 'MINT']
#
# port_data = pdr.get_data_yahoo(symbols, start=start_date, end=end_date)['Adj Close']

import pandas as pd
import numpy as np
from main import root_path
symbols = ['LVMUY', 'FMS', 'GSK', 'NGG', 'AMZN', 'NLY', 'ARCH', 'BAX', 'BA', 'CELH', 'CL', 'XOM', 'GD', 'LMT', 'MDR', 'MRK', 'MU', 'NOC', 'PANW', 'PXD', 'RTN', 'SNAP', 'TSLA', 'VZ', 'WDC', 'UUP', 'VIXY', 'SHY', 'TLT', 'IAU', 'MINT']
allocations = [158, 350, 1106, 228, 8, 419, 287, 288, 70, 2358, 213, 252, 9, 5, 172, 567, 40, 77, 141, 9, 85, 100, 4, 747, 36, 494, 150, 2490, 425, 6768, 1477]
df = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Asset exposure.csv"), index_col = 0)
df.loc['MINT', 'Sector'] = 'Cash'
df.loc['MINT', 'Industry'] = 'Cash'
print df.loc['MINT']

#print portfolio_info
