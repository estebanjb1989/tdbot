from binance.client import Client
from pymongo import MongoClient
import libs.queryService as queryService
import time
from config import api_key, api_secret
import datetime

def generateCommand():
    print("**")
    print("GENERATE COMMAND")
    print("**")

    client = Client(api_key=api_key, api_secret=api_secret,
                    tld="com", testnet=False)

    balance = 0.5
    mongoClient = MongoClient("localhost", 27017)
    db = mongoClient["tdbot"]

    print("Deleting all trade documents...")
    db.trades.delete_many({})

    while (balance > 0):
        threshold = 1.0005
        avg_price = queryService.get_avg_price(client)
        buy_limit_price = queryService.get_buy_limit_price(avg_price=avg_price,
                                                            threshold=threshold)
        sell_limit_price = queryService.get_sell_limit_price(
            avg_price=avg_price, threshold=threshold)

        quantity_btc = 0.1
        quantity_usdt = quantity_btc * avg_price
        quantity_usdt_buy = quantity_btc * buy_limit_price
        quantity_usdt_sell = quantity_btc * sell_limit_price
        profit_usdt = quantity_usdt_sell - quantity_usdt_buy
        profit_ars = profit_usdt * 520
        fee_usdt = profit_usdt * 0.0400
        final_profit_usdt = profit_usdt - (profit_usdt * 0.0400)
        final_profit_ars = final_profit_usdt * 520

        # buyOrder = commandService.create_buy_order_market(quantity)
        # sellOrder = commandService.create_sell_order_limit(quantity, sellLimitPrice)

        data = {
            "symbol": "BTCUSDT",
            "threshold": threshold,
            "created_at": datetime.datetime.now(),
            "avg_price": avg_price,
            "buy_limit_price": buy_limit_price,
            "sell_limit_price": sell_limit_price,
            "quantity_btc": quantity_btc,
            "quantity_usdt": quantity_usdt,
            "quantity_usdt_buy": quantity_usdt_buy,
            "quantity_usdt_sell": quantity_usdt_sell,
            "profit_usdt": profit_usdt,
            'profit_ars': profit_ars,
            "fee_usdt": fee_usdt,
            "final_profit_usdt": final_profit_usdt,
            "final_profit_ars": final_profit_ars,
            "buy_order": "WIP",
            "sell_order": "WIP",
            "status": "open"
        }

        print("Order generated, inserting into trade document...")
        db.trades.insert_one(dict(data))
        balance = balance - quantity_btc
        print("Balance:", balance, "BTC")
        time.sleep(1)
    
generateCommand()