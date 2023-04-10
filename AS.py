import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import shift
from time import sleep
from datetime import datetime, timedelta
import datetime as dt
from threading import Thread
from actions import *



'''
Beginning Account Balances: $1,000,000.00.
Shares can only be traded in lots of 100.
A rebate of 0.002 per share will be paid for executed limit orders, at the end of each competition day.
A fee of 0.003 per share will be charged for executed market orders, at the end of each competition day.
'''


'''
Siyan 04.10.23
# 订单管理
# 止损管理
# log日志
# 归因分析
# 利用MACD，adx指标过滤行情（这不就是技术分析）
'''

def strategy(trader: shift.Trader, ticker: str, endtime):

    initial_pl = trader.get_portfolio_item(ticker).get_realized_pl()
    print(f"initial_pl is {initial_pl}")

    # strategy parameters

    tick_size = 0.01
    num_levels = 10
    transaction_cost = 0.001 # 0.003-0.002
    check_freq = 1 # in second
    order_size = 1  # NOTE: this is 1 lots which is 100 shares.

    i=10
    #while (trader.get_last_trade_time() < endtime):
    while (i):
        i-=1


        # cancel unfilled orders from previous time-step
        cancel_orders(trader, ticker)

        # get necessary data
        best_price = trader.get_best_price(ticker)
        best_bid = best_price.get_bid_price()
        best_ask = best_price.get_ask_price()
        midprice = (best_bid + best_ask) / 2
        
        # we predict price will continue to go down

        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, order_size, best_bid-tick_size)
        print(f"ticker: {ticker}, type: {limit_buy.type}, price: {best_bid-tick_size}")
        trader.submit_order(limit_buy)

        limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, order_size, best_ask+tick_size)
        print(f"ticker: {ticker}, type: {limit_sell.type}, price: {best_ask+tick_size}")
        trader.submit_order(limit_sell)

        #previous_price = midprice
        sleep(check_freq)

    # cancel unfilled orders and close positions for this ticker
    cancel_orders(trader, ticker)
    close_positions(trader, ticker)

    print(
        f"total profits/losses for {ticker}: {trader.get_portfolio_item(ticker).get_realized_pl() - initial_pl}")

    


