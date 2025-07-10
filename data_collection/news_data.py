import os
import requests
import pandas as pd

# CryptoPanic API 키 설정 (환경 변수 또는 직접 입력)
api_key = os.getenv("CRYPTOPANIC_API_KEY")

def get_news_data(filter="important"):
    """
    CryptoPanic API를 통해 뉴스 데이터를 가져옵니다.
    :param filter: "important" 또는 "rising" 등
    :return: pandas DataFrame
    """
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={api_key}&filter={filter}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['results'])
        return df
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

if __name__ == '__main__':
    news_df = get_news_data()
    print(news_df.head())
