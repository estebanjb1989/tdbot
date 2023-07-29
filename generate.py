from binance.client import Client
from pymongo import MongoClient
import time
from config import api_key, api_secret
from business import calculateTrade


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

    threshold = 1.0005
    quantity_btc = 0.1
    fee = 0.0400
    
    while (balance > 0):
        data = calculateTrade(
            client=client,
            threshold=threshold,
            quantity_btc=quantity_btc,
            fee=fee
        )

        print("Order generated, inserting into trade document...")
        db.trades.insert_one(dict(data))
        balance = balance - quantity_btc
        print("Balance:", balance, "BTC")
        time.sleep(1)


generateCommand()
