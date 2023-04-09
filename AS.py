import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import shift
from time import sleep
from datetime import datetime, timedelta
import datetime as dt
from threading import Thread


'''
Beginning Account Balances: $1,000,000.00.
Shares can only be traded in lots of 100.
A rebate of 0.002 per share will be paid for executed limit orders, at the end of each competition day.
A fee of 0.003 per share will be charged for executed market orders, at the end of each competition day.
'''

def AS_strategy(trader: shift.Trader, ticker: str, endtime):
    # NOTE: Unlike the following sample strategy, it is highly reccomended that you track and account for your buying power and
    # position sizes throughout your algorithm to ensure both that have adequite captial to trade throughout the simulation and
    # that you are able to close your position at the end of the strategy without incurring major losses.

    initial_pl = trader.get_portfolio_item(ticker).get_realized_pl()

    # strategy parameters
    check_freq = 1
    order_size = 5  # NOTE: this is 5 lots which is 500 shares.

    # strategy variables
    best_price = trader.get_best_price(ticker)
    best_bid = best_price.get_bid_price()
    best_ask = best_price.get_ask_price()
    previous_price = (best_bid + best_ask) / 2

    while (trader.get_last_trade_time() < endtime):
        # cancel unfilled orders from previous time-step
        cancel_orders(trader, ticker)

        # get necessary data
        best_price = trader.get_best_price(ticker)
        best_bid = best_price.get_bid_price()
        best_ask = best_price.get_ask_price()
        midprice = (best_bid + best_ask) / 2

        # place order
        if (midprice > previous_price):  # price has increased since last timestep
            # we predict price will continue to go up
            order = shift.Order(
                shift.Order.Type.MARKET_BUY, ticker, order_size)
            print(f"ticker: {ticker}, type: {order.type}, price: {midprice}")
            trader.submit_order(order)
        elif (midprice < previous_price):  # price has decreased since last timestep
            # we predict price will continue to go down
            order = shift.Order(
                shift.Order.Type.MARKET_SELL, ticker, order_size)
            print(f"ticker: {ticker}, type: {order.type}, price: {midprice}")
            trader.submit_order(order)
        

            # NOTE: If you place a sell order larger than your current long position, it will result in a short sale, which
            # requires buying power both for the initial short_sale and to close your short position.For example, if we short
            # sell 1 lot of a stock trading at $100, it will consume 100*100 = $10000 of our buying power. Then, in order to
            # close that position, assuming the price has not changed, it will require another $10000 of buying power, after
            # which our pre short-sale buying power will be restored, minus any transaction costs. Therefore, it requires
            # double the buying power to open and close a short position than a long position.

        previous_price = midprice
        sleep(check_freq)

    # cancel unfilled orders and close positions for this ticker
    cancel_orders(trader, ticker)
    close_positions(trader, ticker)

    print(
        f"total profits/losses for {ticker}: {trader.get_portfolio_item(ticker).get_realized_pl() - initial_pl}")
    








# Define model parameters
tick_size = 0.01
num_levels = 10
freq = 1000 # in milliseconds
transaction_cost = 0.0025

# Load order book data
order_book = pd.read_csv('order_book.csv')

# Preprocess order book data
order_book = order_book.dropna() # remove any invalid orders
order_book['price'] = np.round(order_book['price'] / tick_size) * tick_size # round prices to nearest tick
order_book = order_book.groupby('price').agg({'size': 'sum'}).reset_index() # aggregate orders at same price level

# Implement trading strategy
mid_price = (order_book['price'].max() + order_book['price'].min()) / 2
bid_price = mid_price - tick_size
ask_price = mid_price + tick_size
if order_book[order_book['price'] <= bid_price]['size'].sum() >= order_book[order_book['price'] >= ask_price]['size'].sum():
    # place bid order at bid_price
else:
    # place ask order at ask_price

# Simulate trading process
for i in range(len(order_book)):
    # check if trading frequency has elapsed
    if i % (freq / tick_size) == 0:
        # execute trade based on trading strategy
        if # bid order executed:
            # update profit and loss
        elif # ask order executed:
            # update profit and loss

# Evaluate trading strategy

'''Need a log system here.'''

# Compute Sharpe ratio
daily_returns = np.log(trading_results / trading_results.shift(1))
sharpe_ratio = np.sqrt(252) * daily_returns.mean() / daily_returns.std()

# Compute maximum drawdown
cumulative_returns = trading_results / trading_results.iloc[0]
max_drawdown = (cumulative_returns.cummax() - cumulative_returns).max()

# Compute profit factor
profit_factor = trading_results[trading_results > 0].sum() / abs(trading_results[trading_results < 0].sum())

# Compute percentage of profitable trades
pct_profitable = (trading_results > 0).mean()

# Compute average trade duration
avg_trade_duration = trade_duration.mean()