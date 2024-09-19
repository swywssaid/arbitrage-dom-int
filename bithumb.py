import requests
import datetime
import json  
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")

def fetch_bithumb_coin_list():
    try:
        response = requests.get("https://api.bithumb.com/v1/market/all?isDetails=false")
        pretty_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
        return response.json()
    except Exception as e:
        print(f"Error fetching coin list: {e}")

def fetch_bithumb_coin_current_price():
    try:
        response = requests.get("https://api.bithumb.com/v1/ticker", params={"markets": "KRW-BTC"})
        pretty_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
        return response.json()
    except Exception as e:
        print(f"Error fetching current price: {e}")

def fetch_bithumb_coin_minutes_candles(name, to):
    try:
        response = requests.get("https://api.bithumb.com/v1/candles/minutes/60", params={"market": name, "to": to, "count": 200})
        return response.json()
    except Exception as e:
        print(f"Error fetching minutes candles: {e}")

def fetch_bithumb_coin_days_candles(name, to):
    try:
        response = requests.get("https://api.bithumb.com/v1/candles/days", params={"market": name, "to": to, "count": 200})
        pretty_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
        return response.json()
    except Exception as e:
        print(f"Error fetching days candles: {e}")

def fetch_bithumb_coin_months_candles(name):
    """
    두 수를 더한 결과를 반환하는 함수입니다.

    Args:
    name (str): coin's name in market (e.g. BTC-ETH, KRW-ZETA)

    Returns:
    dict: 요청한 마켓의 월별 차트 데이터 (JSON 형식).
    """
    try:
        response = requests.get("https://api.bithumb.com/v1/candles/months", params={"market": name, "count": 200})
        pretty_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
        return response.json()
    except Exception as e:
        print(f"Error fetching months candles: {e}")

def add_month_to_date(date_string):
    date = datetime.datetime.fromisoformat(date_string)
    new_month = (date.month % 12) + 1
    new_year = date.year + (date.month // 12)
    new_date = date.replace(year=new_year, month=new_month)
    return new_date.isoformat()

def calculate_bithumb_listing_date():
    bithumb_coin_list = fetch_bithumb_coin_list()
    print(bithumb_coin_list)
    print("start")
    for coin in bithumb_coin_list:
        # coin['market']: coin's name in market (e.g. BTC-ETH, KRW-ZETA)
        months = fetch_bithumb_coin_months_candles(coin['market'])
        pretty_response = json.dumps(months.json(), indent=4, ensure_ascii=False)
        
        # print(pretty_response)
        months_length = len(months) if len(months) >= 3 else 3
        listing_month = add_month_to_date(months[months_length - 3]["candle_date_time_kst"]) if len(months) == 1 else months[months_length - 3]["candle_date_time_kst"]
        days = fetch_bithumb_coin_days_candles(coin['market'], listing_month)
        days_length = len(days) if len(days) >= 4 else 4
        listing_day = days[days_length - 4]["candle_date_time_kst"]
        prices_by_minutes = fetch_bithumb_coin_minutes_candles(coin['market'], listing_day)
        # print(coin['market'], listing_day, prices_by_minutes)
    #     if len(prices_by_minutes) == 0:
    #         print(coin['market'], prices_by_minutes)
    # print("finish")

def fetch_coinmarketcap_categories():
    try:
        response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories", headers={"X-CMC_PRO_API_KEY": api_key})
        pretty_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
        return response.json()
    except Exception as e:
        print(f"Error fetching Coinmarketcap categories: {e}")

def fetch_coinmarketcap_category():
    try:
        response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/category?id=1", headers={"X-CMC_PRO_API_KEY": api_key})
        pretty_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
        return response.json()
    except Exception as e:
        print(f"Error fetching Coinmarketcap category: {e}")

# Example usage
calculate_bithumb_listing_date()
# fetch_coinmarketcap_category()
