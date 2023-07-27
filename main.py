# main.py
from fastapi import FastAPI
from binance.client import Client
import datetime
from pymongo import MongoClient
import time
import libs.queryService as queryService
import libs.commandService as commandService
from libs.PrettyJSONResponse import PrettyJSONResponse


# PROD
api_key = "69YGe83CyFX9cPbcYgwmNCoqvWNU4G1VYGoKDmPw3aupHi95Ui0IyszGG8gLlnq3"
api_secret = "lDAg2QrNOrXEgTDfAxnNUYSydj2glRdQTOXtOZ4z9vWCLEra8R3eCnOJrZRqNsFu"

# DEMO
# api_key = "Y7G8Cx7NbCfGn7W4dcK4qo51ELc7xLR0UL1jo3lzpTfWZbzQr4PcOM5oJFw89UFp"
# api_secret = "cGNDErNFuTRlwjeFhpHLoqY1BGDugpWRBJSYxfMXLSrRkacBAK9KjqBOYHDgIThh"


app = FastAPI()
client = Client(api_key=api_key, api_secret=api_secret,
                tld="com", testnet=False)
commandService.set_config(api_key=api_key, api_secret=api_secret)


@app.get("/")
async def root():
    return {
        "data": {
            "name": "tdbot-api"
        }
    }


@app.get("/permissions", response_class=PrettyJSONResponse)
async def get_permissions():
    permissions = queryService.get_permissions(client)
    return {
        "data": {
            "permissions": permissions
        }
    }


@app.get("/ticker/{symbol}", response_class=PrettyJSONResponse)
async def get_ticker(symbol: str):
    ticker = queryService.get_symbol_ticker(client, symbol)
    return {
        "data": {
            "ticker": ticker
        }
    }


@app.get("/spot-balance/{asset}", response_class=PrettyJSONResponse)
async def get_spot_balance(asset: str):
    balance = queryService.get_spot_balance(client, asset)
    return {
        "data": {
            "balance": balance
        }
    }


@app.get("/futures-balance", response_class=PrettyJSONResponse)
async def get_futures_balance():
    futuresBalance = queryService.get_futures_balance(client)
    return {
        "data": {
            "futures-balance": futuresBalance
        }
    }


@app.get("/trade", response_class=PrettyJSONResponse)
async def trade():
    balance = 0.5
    mongoClient = MongoClient("localhost", 27017)
    db = mongoClient["tdbot"]

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
            "time": datetime.datetime.now(),
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

        db.trades.insert_one(dict(data))
        balance = balance - quantity_btc
        time.sleep(1)
    return {
        "data": data
    }


@app.get("/simulate", response_class=PrettyJSONResponse)
async def simulate():
    # wip
    mongoClient = MongoClient("localhost", 27017)
    db = mongoClient["tdbot"]
    openOrders = db.trades.find({"status": "open"})
    while len(openOrders) > 0:
        for openOrder in openOrders:
            avg_price = queryService.get_avg_price(client=client)
            if (openOrder["sell_limit_price"] <= avg_price):
                openOrder["status"] = "closed"
                db.trades.update_one({"_id": openOrder["_id"]}, {
                    "$set": {"status": "closed"}})
        openOrders = db.trades.find({"status": "open"})
    return {
        "data": "OK"
    }


@app.get("/constants", response_class=PrettyJSONResponse)
async def get_constants():
    constants = queryService.get_constants(client)
    return {
        "data": {
            "constants": constants
        }
    }
