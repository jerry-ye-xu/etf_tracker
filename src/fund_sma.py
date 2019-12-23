"""
Date: 22/9/19
Author: Jerry Xu
Email: jerryxu2500@gmail.com
"""

# Common Libraries
from collections import deque
import datetime as dt
import requests
import subprocess as sp
from typing import Any, Union, Dict, List, Sequence, Tuple

# Python Wrapper/Github Repositories
from alpha_vantage import timeseries as ts

# Local Python files
from type_hint_objs import JSONType

key_byte_str = sp.run(["cat", "VINTAGE_API_KEY"], capture_output=True).stdout
vintage_api_key = str(key_byte_str, "utf-8")

# https://www.alphavantage.co/query?function=SMA&symbol=MSFT&interval=weekly&time_period=10&series_type=open&apikey=demo

BASE_URL = "https://www.alphavantage.co/query?"
FUNCTION = "function"
SYMBOL = "symbol"
INTERVAL = "interval"
TIME_PERIOD = "time_period"
SERIES_TYPE = "series_type"
OUTPUTSIZE = "outputsize"
APIKEY = "apikey"

JSON_KEY = "Technical Analysis: SMA"

class fund(object):
    """
    Stores information regarding the equity for the last 60 days.

    Fund status: ["lower", "higher"]

    At time of writing (22/12/19), the JSON object returned is as follows:

    {
        "Meta Data": {
            '1: Symbol': <ticker>,
            '2: Indicator': Simple Moving Average (SMA),
            ...
            '7: Time Zone': 'US/Eastern'
        },
        "Technical Analysis: SMA": {
            "YYYY-MM-DD": { 'SMA': <price> },
            "YYYY-MM-DD": { 'SMA': <price> },
            ...
            "YYYY-MM-DD": { 'SMA': <price> },
        }
    }

    Parameter:
    ticker: The ticker symbol of the
    prev_status: Previous status
    time_since_prev_status: Days passed since
    status: Namedtuple regarding whether it is currently below or above the

    historical_data: Previous (60) days of adjusted closing price data stored in queue-like data structure.
    """

    def __init__(self, ticker: str, days_to_store: int) -> None:
        self.ticker = ticker
        self.days_to_store = days_to_store

        self.function = None
        self.interval = None
        self.series_type = None
        self.low_time_period = None
        self.high_time_period = None

        self.status_duration = 0
        self.prev_status = None
        self.status = None
        self.holiday = True

        # We use deque because it automatically "wraps around" when maxlen is reached.
        self.freq_low = deque(maxlen=days_to_store)
        self.freq_high = deque(maxlen=days_to_store)

    def initial_build(
        self,
        function: str, interval: str, series_type: str,
        low_time_period: int, high_time_period: int,
        save_path: str) -> None:

        self.function = function
        self.interval = interval
        self.series_type = series_type
        self.low_time_period = low_time_period
        self.high_time_period = high_time_period

        self.date_format = "%Y-%m-%d"

        self.save_path = save_path

        # differs only with frequency, f"self.file_path_{time_period}.txt"
        self.file_path = f"{save_path}/{self.ticker}_{self.function}"

        self._save_raw_sma_json(
            self.low_time_period,
            self.freq_low
        )
        self._save_raw_sma_json(
            self.high_time_period,
            self.freq_high
        )
        self.status = "lower" if self.freq_low[-1] < self.freq_high[-1] else "higher"

    def build_for_update(self):
        pass

    def update_price(self):
        today = dt.datetime.today().strftime(self.date_format)

        json_sma_low = self._call_api(self.low_time_period)
        json_sma_high = self._call_api(self.high_time_period)

        if json_sma_low is None or json_sma_high is None:
            print("Price could not be updated at this time.")
            return

        try:
            self.freq_low.append(json_sma_low[JSON_KEY][today][self.function])
            self.freq_high.append(json_sma_high[JSON_KEY][today][self.function])

            self.holiday = False

            self._update_price_in_txt(today, self.freq_low)
            self._update_price_in_txt(today, self.freq_high)
        except KeyError:
            print(f"{today} has no new stock prices. Inserting yesterday's stock price.")
            self.freq_low.append(self.freq_low[-1])
            self.freq_high.append(self.freq_high[-1])

            self.holiday = True

        self._update_return_status()

    def define_reporting_params(self) -> None:
        pass

    def report_streak(self) -> None:
        pass

    def _save_raw_sma_json(
        self,
        time_period: int,
        storage: deque) -> None:

        json_file = self._call_api(time_period)

        if json_file is None:
            return

        self._store_raw_json(
            storage,
            json_file
        )
        self._write_to_txt(time_period, json_file)

        return json_file

    def _store_raw_json(
        self,
        storage_deque: deque,
        json_file: JSONType) -> None:

        base = dt.datetime.today()

        date_list = [base - dt.timedelta(days=x) for x in range(self.days_to_store)]
        date_list = [date.strftime(self.date_format) for date in date_list]
        print(f"earliest date is {date_list[-1]}")

        idx = 0
        for date in date_list[::-1]:
            try:
                storage_deque.append(json_file[JSON_KEY][date][self.function])
            except KeyError:
                print(f"Date: {date} contains no information. Utilising price from previous available data.")
                if idx == 0:
                    print(f"idx is {idx}, we need to go back further in time.")
                    found_price = False

                    go_back = 1
                    while not found_price:
                        curr_d = dt.datetime.strptime(date, self.date_format)
                        back_d = curr_d - dt.timedelta(days=go_back)
                        d = back_d.strftime(self.date_format)
                        print(f"date is {d}")
                        try:
                            storage_deque.append(json_file[JSON_KEY][d][self.function])
                            print(f"found first price at {d}")
                            found_price = True
                        except KeyError:
                            go_back += 1
                            # if go_back >= 10:
                            #     found_price = True
                else:
                    storage_deque.append(storage_deque[idx-1])
            idx += 1

        if storage_deque.maxlen != self.days_to_store:
            raise ValueError(f"We have not stored all {self.days_to_store} days.")

    def _call_api(self, time_period: int) -> JSONType:
        api_call = f"{BASE_URL}{FUNCTION}={self.function}&{SYMBOL}={self.ticker}&{INTERVAL}={self.interval}&{TIME_PERIOD}={time_period}&{SERIES_TYPE}={self.series_type}&{APIKEY}={vintage_api_key}"

        res = requests.get(api_call)

        if res.status_code != 200:
            raise ValueError(f"API call was not successful.\nReturned status code {res.status_code}")

        if JSON_KEY not in res.json().keys():
            print(f"API call unsuccessful.\nReturned product is {res.json()}")
            return None

        return res.json()


    def _write_to_txt(self, time_period: int, json_file: JSONType) -> None:
        with open(f"{self.file_path}_{time_period}.txt", "w") as f:
            for k, v in json_file[JSON_KEY].items():
                f.write(f"{k} ")
                f.write(f"{json_file[JSON_KEY][k][self.function]}\n")

    def _update_price_in_txt(self, date, storage, time_period):
        with open(f"{self.file_path}_{time_period}.txt", "r") as f:
            curr = f.read()
        with open(f"{self.file_path}_{time_period}.txt", "w") as f:
            f.write(f"{date} {storage[-1]}")
            f.write(curr)

    # def _write_txt_to_storage(self, time_period):
    #     with open(f"{self.file_path}_{time_period}.txt", "r") as f:
    #         idx = 0
    #         while idx <= 5:
    #             l = f.readline()
    #             print(l)

    def _update_return_status(self) -> None:
        """

        We count the streak for status, resetting if necessary.

        Note, we do not include holidays as part of the streak.

        """

        if self.holiday:
            return

        self.prev_status = self.status
        tmp_status = "lower" if self.freq_low[-1] < self.freq_high[-1] else "higher"

        if tmp_status != self.status:
            self.status_duration = 0
            self.status = tmp_status
        else:
            self.status_duration += 1

if __name__ == "__main__":

    function = "SMA"
    interval = "daily"
    series_type = "close"
    time_period_low = 3
    time_period_high = 10
    save_path = "./data"

    ticker="VEU"

    aapl_fund = fund(ticker=ticker, days_to_store=60)
    # print(aapl_fund.freq_low)

    aapl_fund.initial_build(
        function,
        interval,
        series_type,
        time_period_low,
        time_period_high,
        save_path
    )

    # aapl_fund.update_price()

    # print(aapl_fund.status)
    # print(aapl_fund.status_duration)
    # print(aapl_fund.freq_low[-6])
    # print(aapl_fund.freq_low[-5])
    # print(aapl_fund.freq_low[-4])
    # print(aapl_fund.freq_low[-3])
    # print(aapl_fund.freq_low[-2])
    # print(aapl_fund.freq_low[-1])
    # print(aapl_fund.freq_high[-6])
    # print(aapl_fund.freq_high[-5])
    # print(aapl_fund.freq_high[-4])
    # print(aapl_fund.freq_high[-3])
    # print(aapl_fund.freq_high[-2])
    # print(aapl_fund.freq_high[-1])

    # aapl_fund.update_price()

    # print(aapl_fund.status)
    # print(aapl_fund.status_duration)
    # # print(aapl_fund.freq_low[-3:])
    # # print(aapl_fund.freq_high[-3:])

    # aapl_fund.update_price()

    # # print(aapl_fund.status)
    # # print(aapl_fund.status_duration)
    # # print(aapl_fund.freq_low[-3:])
    # # print(aapl_fund.freq_high[-3:])