import os
from binance.client import Client
from binance import ThreadedWebsocketManager
import pandas as pd
from dotenv import load_dotenv
import time

# .env 파일 로드
load_dotenv()

# 바이낸스 API 키 설정
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# 클라이언트 초기화
client = Client(api_key, api_secret)

def get_historical_data(symbol, interval, start_str, end_str=None):
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(klines, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col])
    return df

def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def process_message(msg):
    if msg.get('e') == '24hrTicker':
        symbol = msg['s']
        price = float(msg['c'])  # 현재 종가
        print(f"Real-time Price for {symbol}: {price}")

def start_websocket_price_stream(symbol):
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()

    # ✅ 올바른 메서드로 수정
    twm.start_symbol_ticker_socket(callback=process_message, symbol=symbol)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nReal-time price stream stopped.")
    finally:
        twm.stop()

if __name__ == '__main__':
    print("Starting real-time price stream for BTCUSDT... Press Ctrl+C to stop.")
    try:
        start_websocket_price_stream("BTCUSDT")
    except Exception as e:
        print(f"Error starting real-time price stream: {e}")
        print("Please ensure your BINANCE_API_KEY and BINANCE_API_SECRET are correctly set in the .env file.")
