# candle_builder.py
import pandas as pd

candles_dict = {}  # {symbol: pd.DataFrame}

def update_candle(symbol, tick, timeframe='1m'):
    if symbol not in candles_dict:
        candles_dict[symbol] = pd.DataFrame(columns=['open','high','low','close','volume'])
    df = candles_dict[symbol]
    # build candle from tick
    # Example: append new row
    df.loc[pd.Timestamp.now()] = [tick['open'], tick['high'], tick['low'], tick['close'], tick['volume']]
    candles_dict[symbol] = df

def get_candles(symbol, timeframe='1m'):
    return candles_dict.get(symbol, pd.DataFrame())
