import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")

pd.options.mode.chained_assignment = None

import yfinance as yf

from datetime import datetime, timedelta

import os
os.chdir("/home/backstreet/use_backtest_bolt")

class BacktestBoltBase():
    ''' Base class for iterative backtesting of trading strategies.

    Attributes
    ==========
    symbol: str
        ticker symbol with which to work with
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval
    amount: float
        initial amount to be invested per trade
    tc: float (default = 0) 
        transaction costs in bips (0.0001)
    use_feather: boolean (default = True) 
        whether to use feather format to load pricing data

    Methods
    =======
    get_data:
        retrieves and prepares the data
    plot_data:
        plots the closing price for the symbol
    get_values:
        returns the date, the price and the spread for the given bar
    print_current_balance:
        prints out the current (cash) balance
    buy_instrument:
        places a buy order
    sell_instrument:
        places a sell order
    print_current_position_value:
        prints out the current position value
    print_current_nav:
        prints out the current net asset value (nav)
    close_pos:
        closes out a long or short position
    '''

    def __init__(self, symbol, start, end, amount, tc = 0, use_feather = True):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_balance = amount
        self.current_balance = amount
        self.units = 0
        self.trades = 0
        self.position = 0
        self.tc = tc * 0.0001
        self.use_feather = use_feather
        self.get_data()

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        if self.use_feather:
            if not os.path.isfile(f'data/feathers/daily/{self.symbol}.feather'):
                ftr_data = yf.download(self.symbol, start=(datetime.now() - timedelta(days=10 * 365)), end=datetime.today())["Adj Close"].to_frame().dropna().reset_index()
                ftr_data.to_feather(f'data/feathers/daily/{self.symbol}.feather')
            raw = pd.read_feather(f'data/feathers/daily/{self.symbol}.feather')
            raw["Date"] = pd.to_datetime(raw["Date"])
            raw.set_index("Date", inplace=True)
        else:
            if not os.path.isfile(f'data/csvs/daily/{self.symbol}.csv'):
                csv_data = yf.download(self.symbol, start=(datetime.now() - timedelta(days=10 * 365)), end=datetime.today())["Adj Close"]
                csv_data.to_csv(f'data/csvs/daily/{self.symbol}.csv')
            raw = pd.read_csv(f'data/csvs/daily/{self.symbol}.csv')
        raw = raw["Adj Close"].to_frame().dropna()
        raw = raw.loc[self.start:self.end].copy()
        raw.rename(columns={"Adj Close" : "price"}, inplace=True)
        raw = raw.loc[self.start:self.end]
        raw["returns"] = np.log(raw.price / raw.price.shift(1))
        self.data = raw

    def reset_data(self):
        self.position = 0
        self.trades = 0
        self.current_balance = self.initial_balance
        self.get_data()

    def plot_data(self, cols = None, title = None):  
        ''' Plots the closing price for the symbol.
        '''
        if cols is None:
            cols = "price"
        if title is None:
            title = self.symbol
        self.data[cols].plot(figsize = (12, 8), title = title)
        # plt.show()
    
    def get_values(self, bar):
        ''' Returns the date, the price and the spread for the given bar.
        '''
        date = str(self.data.index[bar].date())
        price = round(self.data.price.iloc[bar], 5)
        return date, price 
    
    def print_current_balance(self, bar):
        ''' Prints out the current (cash) balance.
        '''
        date, price = self.get_values(bar)
        print("{} | Current Balance: {}".format(date, round(self.current_balance, 2)))
        
    def buy_instrument(self, bar, units = None, amount = None):
        ''' Places a buy order.
        '''
        date, price = self.get_values(bar)
        price += self.tc
        if amount is not None: # use units if units are passed, otherwise calculate units
            units = int(amount / price)
        self.current_balance -= units * price # reduce cash balance by "purchase price"
        self.units += units
        self.trades += 1
        trade_info = "{} |  Buying {} for {}".format(date, units, round(price, 5))
        print(trade_info)
        self.data["trade_info"].iloc[bar] = trade_info
    
    def sell_instrument(self, bar, units = None, amount = None):
        ''' Places a sell order.
        '''
        date, price = self.get_values(bar)
        price -= self.tc
        if amount is not None: # use units if units are passed, otherwise calculate units
            units = int(amount / price)
        self.current_balance += units * price # increases cash balance by "purchase price"
        self.units -= units
        self.trades += 1
        trade_info = "{} |  Selling {} for {}".format(date, units, round(price, 5))
        print(trade_info)
        self.data["trade_info"].iloc[bar] = trade_info
    
    def print_current_position_value(self, bar):
        ''' Prints out the current position value.
        '''
        date, price = self.get_values(bar)
        cpv = self.units * price
        print("{} |  Current Position Value = {}".format(date, round(cpv, 2)))
    
    def print_current_nav(self, bar):
        ''' Prints out the current net asset value (nav).
        '''
        date, price = self.get_values(bar)
        nav = self.current_balance + self.units * price
        print("{} |  Net Asset Value = {}".format(date, round(nav, 2)))
        
    def update_strategy_returns(self, bar):
        date, price = self.get_values(bar)
        value = self.current_balance + (self.units * price)
        value -= (abs(self.units) * self.tc)
        self.data["strategy_returns"].iloc[bar] = value 

    def dump_json(self, fname):
        self.data["Date"] = self.data.index.strftime("%Y%m%d-%H:%M:%S")
        self.data.to_json(f'{self.symbol}_{fname}.json', orient='records')

    def CAGR(self):
        df = self.data.copy()
        n = len(df)/252
        cagr = ((df["cum_return"].to_list()[-1]) ** (1/n)) - 1  
        return cagr

    def volatility(self):
        df = self.data.copy()
        vol = df["daily_ret"].std() * np.sqrt(252)
        return vol

    def max_dd(self):
        df = self.data.copy()
        df["cum_roll_max"] = df["cum_return"].cummax()
        df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
        df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
        max_dd = df["drawdown_pct"].max()
        return max_dd 

    def perf_analysis(self, bar, title=None):
        date, price = self.get_values(bar)
        perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
        self.print_current_balance(bar)
        print("{} | Net performance (%) = {}".format(date, round(perf, 2) ))
        
        # KPIs
        self.data["daily_ret"] = self.data["strategy_returns"].pct_change()
        self.data["cum_return"] = (1 + self.data["daily_ret"]).cumprod()
        
        cagr = self.CAGR() * 100
        print("{} | Compounded Annual Growth Rate (%) = {}".format(date, cagr))

        vol = self.volatility() * 100
        print("{} | Annualized Volatility (%) = {}".format(date, vol))

        sharpe = cagr / vol
        print("{} | Sharpe Ratio = {}".format(date, sharpe))
 
        mdd = self.max_dd() * 100
        print("{} | Maximum Drawdown (%) = {}".format(date, mdd))

        self.data["benchmark_buy_and_hold"] = self.data["returns"].cumsum().apply(np.exp) * self.initial_balance
        self.plot_data(cols=["benchmark_buy_and_hold", "strategy_returns"], title=title)
        print(75 * "-")

    def close_pos(self, bar):
        ''' Closes out a long or short position.
        '''
        date, price = self.get_values(bar)
        print(75 * "-")
        print("{} | +++ CLOSING FINAL POSITION +++".format(date))
        self.current_balance += self.units * price # closing final position (works with short and long!)
        self.current_balance -= (abs(self.units) * self.tc) # substract transactions costs
        self.data["strategy_returns"].iloc[bar] = self.current_balance
        print("{} | closing position of {} for {}".format(date, self.units, price))
        self.units = 0 # setting position to neutral
        self.trades += 1
        print("{} | number of trades executed = {}".format(date, self.trades))



