# Generated by Django 3.0.2 on 2020-01-12 05:30

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

def load_initial_funds(apps, schema_editor):
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
            low_freq_period: int = int(arr[1])
            high_freq_period: int = int(arr[2])
            low_streak_alert: int = int(arr[3])
            high_streak_alert: int = int(arr[4])

            print(f"Loading {ticker} into class object")
            ALL_FUNDS[idx] = fund(ticker, LOGS)
            # print(aapl_fund.freq_low)

            result = ALL_FUNDS[idx].initial_build(
                FUNCTION,
                INTERVAL,
                SERIES_TYPE,
                DAYS_TO_STORE,
                low_freq_period,
                high_freq_period,
                low_streak_alert,
                high_streak_alert,
                SAVE_PATH
            )

            if not result:
                raise ValueError(f"{ALL_FUNDS[idx].ticker} has no stock information. Result returned {result}.")

            # Throw code into database
            print(f"Creating Fund object for DB")
            curr_fund = Fund(
                ticker = ALL_FUNDS[idx].ticker,
                function = ALL_FUNDS[idx].function,
                interval = ALL_FUNDS[idx].interval,
                series_type = ALL_FUNDS[idx].series_type,
                days_to_store = ALL_FUNDS[idx].days_to_store,

                low_freq_period = ALL_FUNDS[idx].low_freq_period,
                high_freq_period = ALL_FUNDS[idx].high_freq_period,
                low_streak_alert = ALL_FUNDS[idx].low_streak_alert,
                high_streak_alert = ALL_FUNDS[idx].high_streak_alert,

                status = ALL_FUNDS[idx].status,
                status_duration = ALL_FUNDS[idx].status_duration,
                prev_status = ALL_FUNDS[idx].prev_status,
                holiday = ALL_FUNDS[idx].holiday
            )

            print(f"Saving {ticker} information to DB")
            curr_fund.save()

            freq_low_list = list(ALL_FUNDS[idx].freq_low)
            freq_high_list = list(ALL_FUNDS[idx].freq_high)
            freq_dates_list = list(ALL_FUNDS[idx].freq_dates)

            print(f"Looping through to create FundPrice objects for DB")
            curr_fund_prices = []
            size = len(freq_low_list)
            for i in range(size):
                curr_fund_price_low = FundPrices(
                    fund=curr_fund,
                    freq_type="low",
                    date=freq_dates_list[i],
                    price=freq_low_list[i],
                )
                curr_fund_price_high = FundPrices(
                    fund=curr_fund,
                    freq_type="high",
                    date=freq_dates_list[i],
                    price=freq_high_list[i],
                )
                curr_fund_prices.append(curr_fund_price_low)
                curr_fund_prices.append(curr_fund_price_high)

            # For every find we create multiple price rows.
            # Hence the .bulk_create()
            print(f"Saving {ticker} prices")
            FundPrices.objects.bulk_create(curr_fund_prices)

            idx += 1
            print(f"Sleeping for {SLEEP_TIME}")
            time.sleep(SLEEP_TIME)

def reverse_initial_funds(apps, schema_editor):
    Fund = apps.get_model("tracker", "Fund")
    FundPrices = apps.get_model("tracker", "FundPrices")

    Fund.objects.all().delete()
    FundPrices.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20200112_0530'),
    ]

    operations = [
        migrations.RunPython(load_initial_funds, reverse_initial_funds)
    ]