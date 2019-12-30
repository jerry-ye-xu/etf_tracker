# Common Libraries
import argparse
import subprocess as sp
import time

from typing import Any, Union, Dict, List, Sequence, Tuple, Optional, Deque

# Local Python files
from fund_sma import fund
from type_hint_objs import JSONType

key_byte_str = sp.run(["cat", "VINTAGE_API_KEY"], capture_output=True).stdout
vintage_api_key = str(key_byte_str, "utf-8")

# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=MSFT&outputsize=compact&apikey=demo

parser = argparse.ArgumentParser(description='Receive csv of funds and frequency to track.')

if __name__ == "__main__":

    tickers_file = "./data/tickers_to_track.csv"

    function = "SMA"
    interval = "daily"
    series_type = "close"
    save_path = "./data"

    days_to_store = 120

    SLEEP_TIME = 2
    HOUR_IN_SECONDS = 60 * 60
    ALL_FUNDS: List[fund] = []
    FAILED_FUNDS = []

    with open(tickers_file, "r") as f:
        for line in f:
            arr = [x.strip() for x in line.split(sep=",")]

            ticker: str = arr[0]
            low_freq_period: int = int(arr[1])
            high_freq_period: int = int(arr[2])
            low_streak_alert: int = int(arr[3])
            high_streak_alert: int = int(arr[4])

            curr_fund = fund(ticker)
            # print(aapl_fund.freq_low)

            result = curr_fund.initial_build(
                function,
                interval,
                series_type,
                days_to_store,
                low_freq_period,
                high_freq_period,
                low_streak_alert,
                high_streak_alert,
                save_path
            )

            if not result:
                FAILED_FUNDS.append(curr_fund.ticker)

            ALL_FUNDS.append(curr_fund)
            time.sleep(SLEEP_TIME)

    if len(FAILED_FUNDS) > 0:
        raise ValueError(f"The following funds could not be found: {FAILED_FUNDS}")

    print("The following tickers have been loaded.")
    for i in range(len(ALL_FUNDS)):
        print(ALL_FUNDS[i].ticker)
        print(ALL_FUNDS[i].report_fund())

    while True:
        for i in range(24):
            print(f"{i}th hour.")
            time.sleep(HOUR_IN_SECONDS)
        for curr_fund in ALL_FUNDS:
            curr_fund.run_daily_update()
            curr_fund.report_fund()