from binance.client import Client
from pymongo import MongoClient
import libs.queryService as queryService
import time
from config import api_key, api_secret
import datetime

def simulateCommand(): 
    print("**")
    print("SIMULATE COMMAND")
    print("**")

    client = Client(api_key=api_key, api_secret=api_secret,
                    tld="com", testnet=False)

    mongoClient = MongoClient("localhost", 27017)
    db = mongoClient["tdbot"]
    openOrders = db.trades.find({"status": "open"})
    while openOrders.collection.count_documents({}) > 0:
        for openOrder in openOrders:
            avg_price = queryService.get_avg_price(client=client)
            print("Average price:", avg_price)
            if (openOrder["sell_limit_price"] <= avg_price):
                print("Sell limit price: ", openOrder["sell_limit_price"])
                print("Limit reached -- closing order")
                openOrder["status"] = "closed"
                openOrder["closed_at"] = datetime.datetime.now(),
                db.trades.update_one({"_id": openOrder["_id"]}, {
                    "$set": {"status": "closed"}})
            else: 
                print("Sell limit price: ", openOrder["sell_limit_price"])
                print("Not reached -- skip")
            time.sleep(10)
        openOrders = db.trades.find({"status": "open"})

simulateCommand()