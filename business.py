import datetime
import queryService as queryService

def calculateTrade(client, threshold, quantity_btc, fee):
    avg_price = queryService.get_avg_price(client)
    buy_limit_price = queryService.get_buy_limit_price(avg_price=avg_price,
                                                       threshold=threshold)
    sell_limit_price = queryService.get_sell_limit_price(
        avg_price=avg_price, threshold=threshold)

    quantity_usdt = quantity_btc * avg_price
    quantity_usdt_buy = quantity_btc * buy_limit_price
    quantity_usdt_sell = quantity_btc * sell_limit_price
    profit_usdt = quantity_usdt_sell - quantity_usdt_buy
    fee_usdt = profit_usdt * fee
    final_profit_usdt = profit_usdt - (profit_usdt * fee)

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
        "fee_usdt": fee_usdt,
        "final_profit_usdt": final_profit_usdt,
        "status": "open"
    }
    return data
