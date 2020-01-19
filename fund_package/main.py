# Common Libraries
import argparse
import logging
import os
import subprocess as sp
import time

from typing import Any, Union, Dict, List, Sequence, Tuple, Optional, Deque

# Local Python files
from fund_sma import fund
from type_hint_objs import JSONType
from logging_obj import LoggerObject

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

# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=MSFT&outputsize=compact&apikey=demo

parser = argparse.ArgumentParser(description='Receive csv of funds and frequency to track.')

if __name__ == "__main__":
    TESTING = False
    tickers_file = "./data/tickers_to_track.csv"

    function = "SMA"
    interval = "daily"
    series_type = "close"
    save_path = "./data"

    days_to_store = 120

    SLEEP_TIME = 2
    HOUR_IN_SECONDS = 60 * 60
    FAILED_FUNDS = []

    with open(tickers_file, "r") as f:
        num_tickers = f.readline()
        print(f"num_tickers: {num_tickers}")
        ALL_FUNDS = [None]*int(num_tickers)
        idx = 0
        for line in f:
            arr = [x.strip() for x in line.split(sep=",")]

            ticker: str = arr[0]
            # Not used.
            ticker_full_name: str = arr[1]
            low_freq_period: int = int(arr[2])
            high_freq_period: int = int(arr[3])
            low_streak_alert: int = int(arr[4])
            high_streak_alert: int = int(arr[5])

            ALL_FUNDS[idx] = fund(ticker, days_to_store, LOGS)
            # print(aapl_fund.freq_low)

            result = ALL_FUNDS[idx].initial_build(
                function,
                interval,
                series_type,
                low_freq_period,
                high_freq_period,
                low_streak_alert,
                high_streak_alert,
                save_path
            )

            if not result:
                FAILED_FUNDS.append(ALL_FUNDS[idx].ticker)

            idx += 1
            time.sleep(SLEEP_TIME)

    if len(FAILED_FUNDS) > 0:
        raise ValueError(f"The following funds could not be found: {FAILED_FUNDS}")

    print("The following tickers have been loaded.")
    for i in range(len(ALL_FUNDS)):
        print(ALL_FUNDS[i].ticker)
        print(ALL_FUNDS[i].report_fund_price())

    while True:
        for i in range(24):
            print(f"{i}th hour.")
            if TESTING:
                time.sleep(2.5) # times 24
            else:
                time.sleep(HOUR_IN_SECONDS)
        print("24 hour wait finished. Now updating funds.")
        for i in range(len(ALL_FUNDS)):
            print(f"ALL_FUNDS[i]: {ALL_FUNDS[i]}")
            print(ALL_FUNDS[i].ticker)
            print(ALL_FUNDS[i].run_daily_update())
            print(ALL_FUNDS[i].report_fund_price())
            print("sleeping for 60 seconds")
            time.sleep(60)

    # For some reason you can't do this.
    # for f in ALL_FUNDS:
    #     print(f)
    #     f.report_fund_price()

    # print("sleeping for 60 seconds")
    # time.sleep(60)

    # for curr_fund in ALL_FUNDS:
    #     print(ALL_FUNDS)
    #     print("run_daily_update")
    #     curr_fund.run_daily_update()
    #     print("report_fund_price")
    #     curr_fund.report_fund_price()
    #     print("finished")
    #     print("sleeping for 60 seconds")
    #     time.sleep(60)

    # while True:
    #     for i in range(24):
    #         print(f"{i}th hour.")
    #         if TESTING:
    #             time.sleep(2.5) # times 24
    #         else:
    #             time.sleep(HOUR_IN_SECONDS)
    #     print("24 hour wait finished. Now updating funds.")
    #     for curr_fund in ALL_FUNDS:
    #         print(ALL_FUNDS)
    #         curr_fund.run_daily_update()
    #         curr_fund.report_fund_price()