# main.py
from config import *
from candle_builder import update_candle
import websocket
import json

# AngelOne websocket connection
def connect_angelone_ws(symbols):
    ws_url = "wss://pushserver.angelbroking.com/..."  # v2 URL
    def on_message(ws, message):
        tick = json.loads(message)
        symbol = tick['symbol']
        update_candle(symbol, tick, '1m')  # update candle in candle builder
        return tick

    ws = websocket.WebSocketApp(ws_url, on_message=on_message)
    ws.run_forever()
    return ws
