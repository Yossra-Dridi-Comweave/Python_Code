import MetaTrader5 as mt5
import pandas as pd
import time

class Explorer:
    def __init__(self, symbol, timeframe, login, password, server):
        self.login = login
        self.password = password
        self.server = server
        self.symbol = symbol
        self.timeframe = timeframe
        self.initialize_mt5()

    def initialize_mt5(self):
        if not mt5.initialize(login=int(self.login), password=self.password, server=self.server):
            print("login ",self.login, "password ", self.password, "server ", self.server)
            print("Initialisation de ljkljljlMT5 a échoué")
            mt5.shutdown()
        else:
            print("MT5 initialisé avec succès")

    def fetch_market_data(self,time_frame):
        """Generic method to fetch market data for a given time frame"""
        self.initialize_mt5()
        print("symbol ",self.symbol)
        print("time_frame ",time_frame)
        prices = mt5.copy_rates_from_pos(self.symbol, time_frame, 0, 200)
        df = pd.DataFrame(prices)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def calculate_ichimoku(self, df):
        """Calculate Ichimoku indicators on the dataframe"""
        df['tenkan_sen'] = (df['high'].rolling(window=9).max() + df['low'].rolling(window=9).min()) / 2
        df['kijun_sen'] = (df['high'].rolling(window=26).max() + df['low'].rolling(window=26).min()) / 2
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
        df['senkou_span_b'] = ((df['high'].rolling(window=52).max() + df['low'].rolling(window=52).min()) / 2).shift(26)
        df['chikou_span'] = df['close'].shift(-26)
        return df[['close', 'high', 'open', 'low', 'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']]
