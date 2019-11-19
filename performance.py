import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as tkr
from main import root_path
import os
import inspect
style.use('ggplot')


def portfolio():
    port_rets = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv"))
    port_data = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Daily_Prices.csv"))
    port_val = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv"))
    bench_rets = pd.read_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Returns.csv"))
    bench_data = pd.read_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Price Data.csv"))
    bench_val = pd.read_csv(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Value.csv")) 
    
    bench_rets.columns = ['Date', 'DJCI', 'DXY', 'SPY', 'TLT', 'Benchmark Value']
    bench_data.columns = ['Date', 'DJCI', 'DXY', 'SPY', 'TLT',]

    if os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv")) and os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Daily_Prices.csv")) \
            and os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv")) and os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv")) \
            and os.path.exists(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Price Data.csv")) and os.path.exists(os.path.join(root_path, "Daily Data", "Benchmark", "Benchmark Returns.csv")):

        if not os.path.exists(os.path.join(root_path, "Figures")):
            os.mkdir(os.path.join(root_path, "Figures"))

        # ----------Plot Performance--------------#
        port_val = port_val.set_index('Date')
        port_values = port_val['Portfolio Value']
        port_values = pd.DataFrame(port_values)
        bench_val = bench_val.set_index('Date')
        bench_values = bench_val['Benchmark Value']
        bench_values = bench_data.set_index('Date')

        #perf = port_values.to_frame().join(bench_data.to_frame())
        perf = pd.merge(port_values, bench_val, left_index=True, right_index=True)
        perf.index = pd.to_datetime(perf.index)

        print(bench_val)
        port_data = perf["Portfolio Value"]
        bench_val = perf["Benchmark Value"]

        fig = plt.figure()
        ax = fig.add_subplot(111, facecolor='#576884')
        lns1 = ax.plot(port_data, linestyle='-', color="white", label='Portfolio')

        # Fill Under
        x = port_data.index
        y = port_data[0:len(port_data)]
        q = bench_data.index
        z = bench_data[0:len(bench_data)]

        ax2 = ax.twinx()
        print(ax.twinx())
        ax2.grid(None)
        lns2 = ax2.plot(bench_val, linestyle='-', color='#6aa527', label='Benchmark')

        # added these three lines
        lns = lns1 + lns2
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=0)
        ax.grid(linestyle='--', alpha=0.2)

        ax.get_yaxis().set_major_formatter(
            tkr.FuncFormatter(lambda x, p: format(int(x), ',')))

        # Annotate Last Price
        bbox_props = dict(boxstyle='round', fc='w', ec='k', lw=1)
        ax.annotate("{:0,.2f}".format(port_val["Portfolio Value"][-1]), (port_val.index[-1], port_val["Portfolio Value"][-1]),
                    xytext=(port_val.index[-1], port_val["Portfolio Value"][-1]), bbox=bbox_props)

        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        plt.suptitle("Portfolio Performance vs. Benchmark")
        plt.savefig(os.path.join(root_path, "Figures", "port_perf.png"))

        call_name = inspect.stack()[1][3]

        if call_name != "perf":
            print('#-------------Fund Performance------------------#')
            print('Fund Performance on: ' + str(port_rets['Date'].iloc[-1]) + ': ' + "{0:.2f}%".format(
                float(port_rets.iloc[-1:, -1]) * 100))
            print('Benchmark Performance on: ' + str(bench_rets['Date'].iloc[-1]) + ': ' + "{0:.2f}%".format(
                float(bench_rets.iloc[-1:, -1]) * 100))
            print('\n')


        return port_rets, bench_rets

    else:
        print('You do not have the necessary data to run this function. Please run the port_data function to import the necessary portfolio data.')


def asset_performance():

    if os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv")) and os.path.exists(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv")):

        port_rets = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Returns.csv"))
        port_val = pd.read_csv(os.path.join(root_path, "Daily Data", "Portfolio", "Portfolio_Value.csv"))

        port_val = port_val.set_index('Date')
        port_rets = port_rets.set_index('Date')

        asset_performance = port_val.iloc[-1] / port_val.iloc[0] - 1
        asset_performance = asset_performance[:-1]
        asset_performance = asset_performance.sort_values(ascending=False)

        top_holdings = port_val.iloc[-1]
        top_holdings = top_holdings[:-1]
        top_holdings = top_holdings.sort_values(ascending=False)

        call_name = inspect.stack()[1][3]

        daily_perf_asset = port_rets.iloc[-1, 0:len(port_rets.columns) - 1]

        if call_name != "perf":
            print('--------Asset Performance Today--------')
            for ticker, val in zip(daily_perf_asset.index, daily_perf_asset):
                print(ticker, "{0:.2f}%".format(val * 100))

            print('--------Top Performers Since Allocation--------')
            for ticker, val in zip(asset_performance.index, asset_performance):
                print(ticker, "{0:.2f}%".format(val * 100))

            print('--------Top Holdings By Dollar Amount--------')
            for ticker, val in zip(top_holdings.index, top_holdings):
                print(ticker, "${:,.2f}".format(val))

        return asset_performance

    else:
        print('You do not have the necessary data to run this function. Please run the port_data function to import the necessary portfolio data.')
