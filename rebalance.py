import pandas as pd
import numpy as np
import os
from main import root_path

def rebalance(allocations):
    if os.path.exists(root_path+'/Daily Data/Portfolio/Portfolio Value.csv') and os.path.exists(root_path+'/Daily Data/Portfolio/Portfolio Daily Prices.csv'):
        port_val = pd.read_csv(root_path + '/Daily Data/Portfolio/Portfolio Value.csv', index_col =0)
        port_prices = pd.read_csv(root_path + '/Daily Data/Portfolio/Portfolio Daily Prices.csv', index_col =0)

        n = len(allocations)
        equity_positions_new = port_val.iloc[-1, 0:n]
        equity_positions_new = equity_positions_new.transpose()

        port_val_new =port_val['Portfolio Value'].iloc[-1]
        weights_new = equity_positions_new/port_val_new

        equity_positions_prior = port_val.iloc[0, 0:n]
        equity_positions_prior = equity_positions_prior.transpose()

        port_val_prior =port_val['Portfolio Value'].iloc[0]
        weights_prior = equity_positions_prior/port_val_prior

        price_data = port_prices.iloc[-1, 0:n]

        allocation_df = pd.DataFrame({'Symbol': weights_prior.index,
                                      'Allocations': allocations}).set_index('Symbol')

        result = pd.concat([allocation_df, price_data, weights_new, weights_prior], axis=1)
        result.columns = ["Original Num Shares", "Current Share Price", "Current Weights", "Weights Prior"]

        result['Status'] = np.where(result['Current Weights'] > result['Weights Prior'], 'Overweight', 'Underweight')

        #Solve for Weights
        solve_weights = []

        for r in range(0, n):
            # share counter
            x = 0.00
            # num shares
            al = result.iloc[r, 0]
            # stock price
            sp = result.iloc[r, 1]
            # equity position
            eq = al * sp
            # Current weight
            cw = eq / port_val_new
            # Over/Under
            status = result.iloc[r, 4]
            # Desired Weight
            dw = result.iloc[r, 3]

            while True:
                # Assumed Formula - this may need to be adjusted to match your criteria
                e = x * sp
                w = e / port_val_new
                x += 0.01

                if status == "Overweight":
                    if w >= dw:
                        solve_weights.append(int(x))
                        break
                    print w
                elif status == "Underweight":
                    if w >= dw:
                        solve_weights.append(int(x))
                        break
                else:
                    break

        solve_weights = pd.DataFrame({'Symbol': weights_prior.index,
                                      'New Share Amount': solve_weights}).set_index('Symbol')

        result = pd.concat([result, solve_weights], axis=1)
        result['# Buy/Sell'] = np.where(result['Status'] == "Overweight",
                                        result['Original Num Shares'] - result['New Share Amount'],
                                        result['New Share Amount'] - result['Original Num Shares'])
        result['Action'] = np.where(result['Status'] == "Overweight", "Sell", "Buy")

        print "---------Number of Shares to Buy/Sell------------"
        print pd.concat([result['Action'], result['# Buy/Sell']], axis=1)

    else:
        print 'You have not downloaded the necessary data to run the rebalance module. Please make sure to run the port_data module.'