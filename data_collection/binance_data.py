import os
from binance.client import Client
import pandas as pd
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 바이낸스 API 키 설정 (환경 변수 또는 직접 입력)
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# 클라이언트 초기화
client = Client(api_key, api_secret)

def get_historical_data(symbol, interval, start_str, end_str=None):
    """
    과거 K-line 데이터를 가져옵니다.
    :param symbol: BTCUSDT, ETHUSDT 등
    :param interval: 1m, 5m, 1h, 1d 등
    :param start_str: "1 Jan, 2020"
    :param end_str: "1 Jan, 2021" (기본값: None)
    :return: pandas DataFrame
    """
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(klines, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    
    # 시간 및 숫자 데이터 타입 변환
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col])
        
    return df

def get_current_price(symbol):
    """
    현재가를 가져옵니다.
    :param symbol: BTCUSDT, ETHUSDT 등
    :return: 현재가 (float)
    """
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

if __name__ == '__main__':
    # BTC/USDT 1일봉 데이터 예시
    # btc_df = get_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2023")
    # print(btc_df.head())

    # BTC/USDT 현재가 테스트
    try:
        current_btc_price = get_current_price("BTCUSDT")
        print(f"Current BTCUSDT Price: {current_btc_price}")
    except Exception as e:
        print(f"Error fetching current price: {e}")
        print("Please ensure your BINANCE_API_KEY and BINANCE_API_SECRET are correctly set in the .env file.")

