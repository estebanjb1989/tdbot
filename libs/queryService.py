def get_permissions(client):
    return client.get_account_api_permissions()


def get_avg_price(client):
    return float(client.get_avg_price(symbol="BTCUSDT", )["price"])


def get_buy_limit_price(avg_price, threshold):
    return avg_price - ((avg_price * threshold) - avg_price)


def get_sell_limit_price(avg_price, threshold):
    return avg_price * threshold


def get_spot_balance(client, asset):
    return client.get_asset_balance(asset=asset)


def get_futures_balance(client):
    return client.futures_account_balance()


def get_symbol_ticker(client, symbol):
    return client.get_symbol_ticker(symbol=symbol)


def get_constants(client):
    return {
        'sideBuy': client.SIDE_BUY,
        'type': client.ORDER_TYPE_LIMIT,
        'timeInForce': client.TIME_IN_FORCE_GTC
    }
