# Common Libraries
import argparse
import time

# Local Python files
from fund_sma import *
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
    ALL_FUNDS = []

    with open(tickers_file, "r") as f:
        for line in f:
            arr = [x.strip() for x in line.split(sep=",")]

            ticker = arr[0]
            low_freq_period = arr[1]
            high_freq_period = arr[2]
            low_streak_alert = arr[3]
            high_streak_alert = arr[4]

            curr_fund = fund(ticker)
            # print(aapl_fund.freq_low)

            curr_fund.initial_build(
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

            ALL_FUNDS.append(curr_fund)
            time.sleep(SLEEP_TIME)

    print("The following tickers have been loaded.")
    for i in range(len(ALL_FUNDS)):
        print(ALL_FUNDS[i].ticker)

    while True:
        for i in range(24):
            print(f"{i}th hour.")
            time.sleep(hour_in_seconds)
        for fund in ALL_FUNDS:
            fund.run_daily_update()