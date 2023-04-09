def print_all_orders(trader):
        print(trader.get_last_trade_time())
        print("  Price\t\tSize\t  Dest\t\tTime")
        print("GLOBAL_BID")
        for order in trader.get_order_book("AAPL", shift.OrderBookType.GLOBAL_BID, 50):
            
            print(
                "%7.2f\t\t%4d\t%6s\t\t%19s"
                % (order.price, order.size, order.destination, order.time)
            )
        print()
        print("GLOBAL_ASK")
        for order in trader.get_order_book("AAPL", shift.OrderBookType.GLOBAL_ASK, 50):
            
            print(
                "%7.2f\t\t%4d\t%6s\t\t%19s"
                % (order.price, order.size, order.destination, order.time)
            )

        print()
        for order in trader.get_order_book("AAPL", shift.OrderBookType.LOCAL_BID, 5):
            print("LOCAL_BID")
            print(
                "%7.2f\t\t%4d\t%6s\t\t%19s"
                % (order.price, order.size, order.destination, order.time)
            )        
        print()
        for order in trader.get_order_book("AAPL", shift.OrderBookType.LOCAL_ASK, 5):
            print("LOCAL_ASK")
            print(
                "%7.2f\t\t%4d\t%6s\t\t%19s"
                % (order.price, order.size, order.destination, order.time)
            )



def print_all_prices(best_price):
        print(best_price.get_bid_price())
        print(best_price.get_bid_size())
        print(best_price.get_ask_price())
        print(best_price.get_ask_size())
        print(best_price.get_global_bid_price())
        print(best_price.get_global_bid_size())
        print(best_price.get_global_ask_price())
        print(best_price.get_global_ask_size())
        print(best_price.get_local_bid_price())
        print(best_price.get_local_bid_size())
        print(best_price.get_local_ask_price())
        print(best_price.get_local_ask_size())