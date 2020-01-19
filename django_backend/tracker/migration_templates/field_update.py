from django.db import migrations

import datetime as dt
import logging
import time

from django.db import migrations

from fund_sma import fund
from logging_obj import LoggerObject

DATA_PATH = "../data"
SAVE_PATH = DATA_PATH # For clarity
FUND_CSV_PATH = f"{DATA_PATH}/tickers_to_track.csv"
FUNCTION = "SMA"
INTERVAL = "daily"
SERIES_TYPE = "close"
DAYS_TO_STORE = 120

SLEEP_TIME = 20

FORMAT = "%(asctime)s: %(name)s - %(levelname)s\n %(message)s"

LOGS = LoggerObject(name="logging_object", level=logging.DEBUG)
LOGS.add_handler(
    level=logging.ERROR,
    formatting=FORMAT,
    handler=logging.StreamHandler,
    name=None
)
LOGS.add_handler(
    level=logging.DEBUG,
    formatting=FORMAT,
    handler=logging.FileHandler,
    name="sma_fund.log"
)

def update_field_of_funds(apps, schema_editor):
    Fund = apps.get_model("tracker", "Fund")
    FundPrices = apps.get_model("tracker", "FundPrices")

    with open(FUND_CSV_PATH, 'r') as f:
        num_tickers = f.readline()
        print(f"num_tickers: {num_tickers}")
        ALL_FUNDS = [None]*int(num_tickers)
        idx = 0
        for line in f:
            arr = [x.strip() for x in line.split(sep=",")]

            ticker: str = arr[0]
            ticker_full_name: str = arr[1]
            low_freq_period: int = int(arr[2])
            high_freq_period: int = int(arr[3])
            low_streak_alert: int = int(arr[4])
            high_streak_alert: int = int(arr[5])

            print(f"Saving {ticker} information to DB")
            curr = Fund.objects.get(ticker=ticker)
            curr.most_recent_date = dt.datetime.today()
            curr.save()

            print(f"Information saved for {curr.ticker}.")
            print(f"{curr.ticker}'s full name is {curr.ticker_full_name}.")

            idx += 1
            print(f"Sleeping for {SLEEP_TIME}")
            time.sleep(SLEEP_TIME)

def reverse_initial_funds(apps, schema_editor):
    Fund = apps.get_model("tracker", "Fund")
    FundPrices = apps.get_model("tracker", "FundPrices")

    Fund.objects.all().delete()
    FundPrices.objects.all().delete()

class Migration(migrations.Migration):

    # This needs to change
    dependencies = [
        # ('tracker', '0006_fund_most_recent_date'),
    ]

    operations = [
        # migrations.RunPython(update_field_of_funds, reverse_initial_funds)
    ]
