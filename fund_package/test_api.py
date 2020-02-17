import datetime as dt
import logging
import os
import requests
import time

from fund_sma import fund

vantage_api_key = os.environ.get('VANTAGE_API_KEY')
if vantage_api_key is None:
    raise ValueError("vantage_api_key not set as environment variable!")

BASE_URL = "https://www.alphavantage.co/query?"
FUNCTION = "function"
SYMBOL = "symbol"
INTERVAL = "interval"
TIME_PERIOD = "time_period"
SERIES_TYPE = "series_type"
OUTPUTSIZE = "outputsize"
APIKEY = "apikey"

JSON_KEY = "Technical Analysis: SMA"

function = "SMA"
interval = "daily"
series_type = "close"
days_to_store = 120
low_freq_period = 3
high_freq_period = 10
low_streak_alert = 1
high_streak_alert = 5
save_path = "./data"

ticker="SPY"
time_period = low_freq_period

api_call = f"{BASE_URL}{FUNCTION}={function}&{SYMBOL}={ticker}&{INTERVAL}={interval}&{TIME_PERIOD}={time_period}&{SERIES_TYPE}={series_type}&{APIKEY}={vantage_api_key}"

print(f"api_call is: {api_call}")

res = requests.get(api_call)

print(res.status_code)
print(res.json().keys())
if "Error Message" in res.json().keys():
    print(res.json()["Error Message"])