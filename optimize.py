import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import os
from main import root_path
style.use('ggplot')

def min_var(symbols):

    if os.path.exists(root_path + '/Daily Data/Portfolio/Portfolio Returns.csv'):
        port_rets = pd.read_csv(root_path + '/Daily Data/Portfolio/Portfolio Returns.csv', index_col= 0)

        n = len(port_rets.columns) - 1
        returns = port_rets.iloc[:,0:n]

        cov_matrix = returns.cov()
        mean_daily_returns = returns.mean()

        # set number of runs of random portfolio weights
        num_portfolios = 25000

        # set up array to hold results
        # We have increased the size of the array to hold the weight values for each stock
        results = np.zeros((4 + len(symbols) - 1, num_portfolios))

        for i in xrange(num_portfolios):
            # select random weights for portfolio holdings
            weights = np.array(np.random.random(len(symbols)))

            # rebalance weights to sum to 1
            weights /= np.sum(weights)

            # calculate portfolio return and volatility
            portfolio_return = np.sum(mean_daily_returns * weights) * 252
            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)

            # store results in results array
            results[0, i] = portfolio_return
            results[1, i] = portfolio_std_dev

            # store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
            results[2, i] = results[0, i] / results[1, i]

           # iterate through the weight vector and add data to results array
            for j in range(len(weights)):
                results[j + 3, i] = weights[j]

        # convert results array to Pandas DataFrame
        flds = ['ret', 'stdev', 'sharpe']
        lista = flds + symbols
        results_frame = pd.DataFrame(results.T,
                                     columns=lista)

        # locate position of portfolio with highest Sharpe Ratio
        max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
        # locate positon of portfolio with minimum standard deviation
        min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

        print results_frame

        print "-------------Max Sharpe Portfolio------------"
        print(max_sharpe_port)
        print '\n'
        print "-------------Minimum Variance Portfolio------------"
        print(min_vol_port)

        plt.scatter(results_frame.stdev, results_frame.ret, c=results_frame.sharpe, cmap='plasma')
        plt.title('Efficient Froniter of a ' + str(len(symbols)) + ' Asset Portfolio', fontsize=14, fontweight='bold', y=1.02)
        plt.xlabel('Risk')
        plt.ylabel('Return')
        clb = plt.colorbar()
        clb.ax.set_ylabel('Sharpe Ratio Value', color='Black')
        plt.scatter(max_sharpe_port[1], max_sharpe_port[0], marker='o', color='b', s=20, label='Tangent Portfolio')
        plt.scatter(min_vol_port[1], min_vol_port[0], marker='o', color='r', s=20, label='Minimum Variance Portfolio')
        plt.legend(loc='upper left', fontsize='small')
        plt.show()

    else:
        print 'You have not downloaded data for your portfolio yet in oder for the optimization module to be run. Please download the data by running the following function --- port_data.portfolio_daily_data()'

