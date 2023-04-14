import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import shift
from time import sleep
from datetime import datetime, timedelta
import datetime as dt
from threading import Thread
import actions



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

def get_Reservation_price(midprice, order_size, T_t):
    '''
    r = s - qγσ^2(T-t)

    s = current market mid price
    q = quantity of assets in inventory of base asset (could be positive/negative for long/short positions)
        power = 1,000,000 / 2
        the value of q is calculated based on the target inventory percentage you are aiming for.


    σ = market volatility
        volatility value depends on the market price movement
        std for now.

    T = closing time, when the measurement period ends (conveniently normalized to 1)
    t = current time (T is normalized = 1, so t is a time fraction)
    γ = inventory risk aversion parameter
        must be defined by the market maker
    κ = order book liquidity parameter
    see details in the parper.

    '''
    # The Wiener process parameter.
    sigma = 2
    # Risk factor (->0: high risk, ->1: low risk)
    gamma = 0.1
    # Market model
    k = 10

    reservation_price = midprice - order_size * gamma * sigma**2 * (T_t)
    return reservation_price

def get_Optimal_bid_ask_spread(T_t):
    '''
    δa + δb = γσ^2(T-t) + 2/γln(1+ γ/κ)

    s = current market mid price
    q = quantity of assets in inventory of base asset (could be positive/negative for long/short positions)
    σ = market volatility

    T = closing time, when the measurement period ends (conveniently normalized to 1)
    t = current time (T is normalized = 1, so t is a time fraction)
    γ = inventory risk aversion parameter

    κ = order book liquidity parameter


    Computation of spread for a symmetric strategy
    '''

    sigma = 2
    gamma = 0.1
    k = 10

    spread = gamma * sigma**2 * (T_t) +  (2 / gamma) * np.log(1 + (gamma / k))
    spread /= 2

    return spread


def strategy(trader: shift.Trader, ticker: str, current, starttime, endtime):

    initial_pl = trader.get_portfolio_item(ticker).get_realized_pl()
    print(f"initial_pl is {initial_pl}")

    # strategy parameters

    tick_size = 0.01
    num_levels = 10
    transaction_cost = 0.001 # 0.003-0.002
    check_freq = 10 # in second
    order_size = 1  # NOTE: this is 1 lots which is 100 shares.
    T_t = (endtime - current)/(endtime-starttime)
    print(T_t)
    i=1000
    #while (trader.get_last_trade_time() < endtime):
    while (i):
        i-=1


        # cancel unfilled orders from previous time-step
        actions.cancel_orders(trader, ticker)

        # get necessary data
        best_price = trader.get_best_price(ticker)
        best_bid = best_price.get_bid_price()
        best_ask = best_price.get_ask_price()
        midprice = (best_bid + best_ask) / 2
        reservation_price = get_Reservation_price(midprice, order_size, T_t)
        spread = get_Optimal_bid_ask_spread(T_t)
        if reservation_price >= midprice:
            ask_spread = spread + (reservation_price - midprice)
            bid_spread = spread - (reservation_price - midprice)
        else:
            ask_spread = spread - (midprice - reservation_price)
            bid_spread = spread + (midprice - reservation_price)
        print(f"ask_spread{ask_spread}, bid_spread{bid_spread}")
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, ticker, order_size, best_bid-bid_spread)
        print(f"ticker: {ticker}, type: {limit_buy.type}, price: {best_bid-bid_spread}, best_bid{best_bid} ")
        trader.submit_order(limit_buy)

        limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, ticker, order_size, best_ask+ask_spread)
        print(f"ticker: {ticker}, type: {limit_sell.type}, price: {best_ask+ask_spread}, best_ask{best_ask}")
        trader.submit_order(limit_sell)



        #previous_price = midprice
        sleep(check_freq)

    # cancel unfilled orders and close positions for this ticker
    # print(
    # "Symbol\t\t\t\tType\t  Price\t\tSize\tExecuted\tID\t\t\t\t\t\t\t\t\t\t\t\t\t\t Status\t\tTimestamp"
    # )
    # for order in trader.get_waiting_list():
    #     print(
    #         "%6s\t%16s\t%7.2f\t\t%4d\t\t%4d\t%36s\t%23s\t\t%26s"
    #         % (
    #             order.symbol,
    #             order.type,
    #             order.price,
    #             order.size,
    #             order.executed_size,
    #             order.id,
    #             order.status,
    #             order.timestamp,
    #         )
    #     )


    actions.cancel_orders(trader, ticker)
    actions.close_positions(trader, ticker)



    # print("Buying Power\tTotal Shares\tTotal P&L\tTimestamp")
    # print(
    #     "%12.2f\t%12d\t%9.2f\t%26s"
    #     % (
    #         trader.get_portfolio_summary().get_total_bp(),
    #         trader.get_portfolio_summary().get_total_shares(),
    #         trader.get_portfolio_summary().get_total_realized_pl(),
    #         trader.get_portfolio_summary().get_timestamp(),
    #     )
    # )

    print(
        f"total profits/losses for {ticker}: {trader.get_portfolio_item(ticker).get_realized_pl() - initial_pl}")

    


