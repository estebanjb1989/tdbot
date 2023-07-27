from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from binance.client import Client
import libs.queryService as queryService
import libs.commandService as commandService
from libs.PrettyJSONResponse import PrettyJSONResponse
from config import api_key, api_secret
import datetime

app = FastAPI()
client = Client(api_key=api_key, api_secret=api_secret,
                tld="com", testnet=False)
commandService.set_config(api_key=api_key, api_secret=api_secret)
templates = Jinja2Templates(directory="templates/")


def calculateTrade(threshold, quantity_btc):
    avg_price = queryService.get_avg_price(client)
    buy_limit_price = queryService.get_buy_limit_price(avg_price=avg_price,
                                                       threshold=threshold)
    sell_limit_price = queryService.get_sell_limit_price(
        avg_price=avg_price, threshold=threshold)

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
    return data


@app.get("/")
async def root(request: Request):
    result = "Calculator"
    return templates.TemplateResponse('calculator.html', context={'request': request, 'result': result})


@app.post("/")
def form_post(request: Request, threshold: str = Form(...), quantity_btc: str = Form(...)):
    result = calculateTrade(threshold=float(threshold),
                            quantity_btc=float(quantity_btc))
    return templates.TemplateResponse('calculator.html',
                                      context={
                                          'request': request,
                                          'result': result,
                                          'threshold': threshold,
                                          'quantity_btc': quantity_btc,
                                          'buy_limit_price': result["buy_limit_price"],
                                          'sell_limit_price': result["sell_limit_price"],
                                          'final_profit_usdt': result["final_profit_usdt"]
                                      })


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


@app.get("/constants", response_class=PrettyJSONResponse)
async def get_constants():
    constants = queryService.get_constants(client)
    return {
        "data": {
            "constants": constants
        }
    }
