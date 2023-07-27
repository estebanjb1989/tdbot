# main.py
from fastapi import FastAPI
from binance.client import Client
import libs.queryService as queryService
import libs.commandService as commandService
from libs.PrettyJSONResponse import PrettyJSONResponse
from config import api_key, api_secret

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


@app.get("/constants", response_class=PrettyJSONResponse)
async def get_constants():
    constants = queryService.get_constants(client)
    return {
        "data": {
            "constants": constants
        }
    }
