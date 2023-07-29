from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from binance.client import Client
import queryService
import commandService
from libs.PrettyJSONResponse import PrettyJSONResponse
from config import api_key, api_secret
from business import calculateTrade

app = FastAPI()
client = Client(api_key=api_key, api_secret=api_secret,
                tld="com", testnet=False)
commandService.set_config(api_key=api_key, api_secret=api_secret)
templates = Jinja2Templates(directory="templates/")


@app.get("/")
async def root(request: Request):
    result = "Calculator"
    return templates.TemplateResponse('calculator.html', context={'request': request, 'result': result})


@app.post("/")
def form_post(request: Request, threshold: str = Form(...), quantity_btc: str = Form(...)):
    result = calculateTrade(client=client,
                            threshold=float(threshold),
                            quantity_btc=float(quantity_btc),
                            fee=0.0400)

    return templates.TemplateResponse('calculator.html',
                                      context={
                                          'request': request,
                                          'result': result,
                                          'threshold': threshold,
                                          'quantity_btc': quantity_btc,
                                          'avg_price': result["avg_price"],
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
