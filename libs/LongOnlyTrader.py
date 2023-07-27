from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from binance import ThreadedWebsocketManager
from binance.client import Client
# import pickle
# import io

class LongOnlyTrader():
    def __init__(
        self,
        symbol,
        bar_length,
        return_thresh,
        volume_thresh,
        units,
        position,
        api_key,
        api_secret,
        bot,
        message_callback,
        chat_id,
    ):
        self.symbol = symbol
        self.bar_length = bar_length
        self.data = pd.DataFrame(
            columns=["Open", "High", "Low", "Close", "Volume", "Complete"])
        self.available_intervals = [
            "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h"]

        self.units = units
        self.position = position

        # strategy-specific attributes
        self.return_thresh = return_thresh
        self.volume_thresh = volume_thresh

        # creds
        self.api_key = api_key
        self.api_secret = api_secret

        self.message_callback = message_callback
        self.chat_id = chat_id
        self.bot = bot

    def start_trading(self, historical_days):
        self.client = Client(
            api_key=self.api_key, api_secret=self.api_secret, tld="com", testnet=True)
        self.twm = ThreadedWebsocketManager(
            api_key=self.api_key, api_secret=self.api_secret)
        self.twm.start()

        self.message_callback(self.chat_id, "Starting trading process")
        # account = self.client.get_account()
        # print(account)

        if self.bar_length in self.available_intervals:
            self.get_most_recent(
                symbol=self.symbol, interval=self.bar_length, days=historical_days)
            self.twm.start_kline_socket(callback=self.stream_candles,
                                        symbol=self.symbol, interval=self.bar_length)
            self.twm.join()

    def get_most_recent(self, symbol, interval, days):
        now = datetime.utcnow()
        past = str(now - timedelta(days=days))

        bars = self.client.get_historical_klines(symbol=symbol, interval=interval,
                                                 start_str=past, end_str=None, limit=1000)

        df = pd.DataFrame(bars)
        df["Date"] = pd.to_datetime(df.iloc[:, 0], unit="ms")
        df.columns = ["Open Time", "Open", "High", "Low", "Close", "Volume",
                      "Close Time", "Quote Asset Volume", "Number of Trades",
                      "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore", "Date"]
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
        df.set_index("Date", inplace=True)
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        df["Complete"] = [True for row in range(len(df)-1)] + [False]

        self.data = df  # create self.data

    def stream_candles(self, msg):
        # extract the required items from msg
        event_time = pd.to_datetime(msg["E"], unit="ms")
        start_time = pd.to_datetime(msg["k"]["t"], unit="ms")
        first = float(msg["k"]["o"])
        high = float(msg["k"]["h"])
        low = float(msg["k"]["l"])
        close = float(msg["k"]["c"])
        volume = float(msg["k"]["v"])
        complete = msg["k"]["x"]

        str = "Time: {} | Price: {}".format(event_time, close)
        print(str)
        # self.message_callback(self.chat_id, str)
        # print(".", end = "", flush = True)

        # feed df (add new bar/update latest bar)
        self.data.loc[start_time] = [first, high, low, close, volume, complete]

        # prepare features and define strat/trading positions whenever the latest bar is complete
        if complete == True:
            # self.message_callback(self.chat_id, self.data.to_csv())
            # my_bytes = pickle.dumps(self.data, protocol=4)
            # file_obj = io.BytesIO(my_bytes)
            # file_obj.name = "data.xlsx"
            # self.bot.send_document(self.chat_id, file_obj)

            self.define_strategy()
            self.execute_trades()

    def define_strategy(self):

        df = self.data.copy()

        # definition of strategy
        df = df[["Close", "Volume"]].copy()
        df["returns"] = np.log(df.Close / df.Close.shift())
        df["vol_ch"] = np.log(df.Volume.div(df.Volume.shift(1)))
        df.loc[df.vol_ch > 3, "vol_ch"] = np.nan
        df.loc[df.vol_ch < -3, "vol_ch"] = np.nan

        cond1 = df.returns >= self.return_thresh
        cond2 = df.vol_ch.between(self.volume_thresh[0], self.volume_thresh[1])

        df["position"] = 1
        df.loc[cond1 & cond2, "position"] = 0

        self.prepared_data = df.copy

    def execute_trades(self):
        # if position is long -> go/stay long
        if self.prepared_data()["position"].iloc[-1] == 1:
            if self.position == 0:
                order = self.client.create_order(
                    symbol=self.symbol, side="BUY", type="MARKET", quantity=self.units)
                self.message_callback(self.chat_id, "GOING LONG")
                self.message_callback(self.chat_id, order)
            self.position = 1
        # if position is neutral -> go/stay neutral
        elif self.prepared_data()["position"].iloc[-1] == 0:
            if self.position == 1:
                order = self.client.create_order(
                    symbol=self.symbol, side="SELL", type="MARKET", quantity=self.units)
                self.message_callback(self.chat_id, "GOING NEUTRAL")
                self.message_callback(self.chat_id, order)
            self.position = 0

# def create_buy_order(client, limitPrice):
#     order = {
#         "side": client.SIDE_BUY,
#         "symbol": "BTCUSDT",
#         "quantity": 0.0001,
#         "type": client.ORDER_TYPE_LIMIT,
#         "timeInForce": client.TIME_IN_FORCE_GTC,
#         "price": limitPrice,
#     }
#     client.futures_create_order(args=order)
#     return order


# def create_sell_order(client, limitPrice):
#     order = {
#         "side": client.SIDE_SELL,
#         "symbol": "BTCUSDT",
#         "quantity": 0.0001,
#         "type": client.ORDER_TYPE_LIMIT,
#         "timeInForce": client.TIME_IN_FORCE_GTC,
#         "price": limitPrice
#     }
#     client.futures_create_order(args=order)
#     return order