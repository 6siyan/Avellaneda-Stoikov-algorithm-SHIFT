import shift
from time import sleep
from datetime import datetime, timedelta
import datetime as dt
from threading import Thread
from actions import *
from AS import *

# NOTE: for documentation on the different classes and methods used to interact with the SHIFT system, 
# see: https://github.com/hanlonlab/shift-python/wiki


def main(trader):
    # keeps track of times for the simulation
    check_frequency = 60
    current = trader.get_last_trade_time()
    start_time = datetime.combine(current, dt.time(9, 35, 0))
    end_time = datetime.combine(current, dt.time(15, 45, 0))
    #start_time = current
    #end_time = start_time + timedelta(minutes=1)

    while trader.get_last_trade_time() < start_time:
        print("still waiting for market open")
        sleep(check_frequency)

    # we track our overall initial profits/losses value to see how our strategy affects it
    initial_pl = trader.get_portfolio_summary().get_total_realized_pl()

    threads = []

    # in this example, we simultaneously and independantly run our trading alogirthm on two tickers
    tickers = ['NKE', 'AAPL', 'MSFT', 'AMZN']

    print("START")

    for ticker in tickers:
        # initializes threads containing the strategy for each ticker
        threads.append(
            Thread(target=strategy, args=(trader, ticker, current, start_time, end_time)))

    for thread in threads:
        thread.start()
        sleep(1)

    # wait until endtime is reached
    while trader.get_last_trade_time() < end_time:
        sleep(check_frequency)

    # wait for all threads to finish
    for thread in threads:
        # NOTE: this method can stall your program indefinitely if your strategy does not terminate naturally
        # setting the timeout argument for join() can prevent this
        thread.join()

    # make sure all remaining orders have been cancelled and all positions have been closed
    for ticker in tickers:
        cancel_orders(trader, ticker)
        close_positions(trader, ticker)

    print("END")
    print(f"final bp: {trader.get_portfolio_summary().get_total_bp()}")
    print(
        f"final profits/losses: {trader.get_portfolio_summary().get_total_realized_pl() - initial_pl}")


if __name__ == '__main__':
    with shift.Trader("slurpupalpha") as trader:
        trader.connect("initiator.cfg", "o0jFo1o0n0")
        sleep(1)
        trader.sub_all_order_book()
        sleep(1)
        main(trader)
