"""
Date: 22/9/19
Author: Jerry Xu
Email: jerryxu2500@gmail.com
"""

# Common Libraries
from collections import deque
import datetime as dt
import json
import logging
import requests
import subprocess as sp
import time
from typing import Any, Union, Dict, List, Sequence, Tuple, Optional, Deque

# Python Wrapper/Github Repositories
from alpha_vantage import timeseries as ts

# Local Python files
from type_hint_objs import JSONType
from logging_obj import LoggerObject

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

    def __init__(self, ticker: str, logs: LoggerObject) -> None:
        self.ticker = ticker
        self.logs = logs

        self.status_duration = 0
        self.prev_status: Any = None # for redefinitions

    def initial_build(
        self,
        function: str, interval: str,
        series_type: str, days_to_store: int,
        low_freq_period: int, high_freq_period: int,
        low_streak_alert: int, high_streak_alert: int,
        save_path: str) -> bool:

        self.function = function
        self.interval = interval
        self.series_type = series_type
        self.days_to_store = days_to_store

        self.low_freq_period = low_freq_period
        self.high_freq_period = high_freq_period
        self.low_streak_alert = low_streak_alert
        self.high_streak_alert = high_streak_alert

        # We use deque because it automatically "wraps around" when maxlen is reached.
        self.freq_low: Deque[float] = deque(maxlen=self.days_to_store)
        self.freq_high: Deque[float] = deque(maxlen=self.days_to_store)

        self.date_format = "%Y-%m-%d"

        self.save_path = save_path

        # differs only with frequency, f"self.file_path_{time_period}.txt"
        self.file_path = f"{save_path}/{self.ticker}_{self.function}"

        success_one = self._save_raw_sma_json(
            self.low_freq_period,
            self.freq_low
        )
        success_two = self._save_raw_sma_json(
            self.high_freq_period,
            self.freq_high
        )
        self.logs.logger.info("Saved raw SMA data to json.")

        if success_one and success_two:
            self.status = "lower" if self.freq_low[-1] < self.freq_high[-1] else "higher"
        else:
            return False
        self.logs.logger.info(f"Set self.status to {self.status} during initialisation.")

        self._backup_var_to_json()

        return True

    def run_daily_update(self) -> str:

        self.logs.logger.info(f"Running daily update for {self.ticker}")
        self._backup_var_to_json() # backup before updating
        self.update_price()

        self.logs.logger.info(f"Finished daily update for {self.ticker}, now reporting streak.")
        return self.report_streak()

    def update_price(self) -> None:
        today = dt.datetime.today().strftime(self.date_format)

        json_sma_low = self._call_api(self.low_freq_period)
        json_sma_high = self._call_api(self.high_freq_period)

        if json_sma_low is None or json_sma_high is None:
            self.logs.logger.error(f"Price for {self.ticker} could not be updated at this time.\nThe call to API returned an error perhaps?")
            return

        try:
            self.freq_low.append(json_sma_low[JSON_KEY][today][self.function]) # type: ignore
            self.freq_high.append(json_sma_high[JSON_KEY][today][self.function]) # type: ignore

            self.holiday = False

            self._update_price_in_txt(today,
                self.freq_low,
                self.low_freq_period
            )
            self._update_price_in_txt(today,
                self.freq_high,
                self.high_freq_period
            )
            self.logs.logger.info("API call successful. Today's prices updated.")

        except KeyError:
            self.logs.logger.info(f"{today} has no new stock prices. Inserting yesterday's stock price.")
            self.freq_low.append(self.freq_low[-1])
            self.freq_high.append(self.freq_high[-1])

            self.holiday = True

        self._update_return_status()
        self.logs.logger.info("update_price() finished.")

    def define_reporting_params(self) -> None:
        pass

    def report_fund(self) -> str:
        """

        Report the sticker and today's prices

        """

        # fund_price_and_ticker = f"{self.ticker} prices today are:\n\t\tSMA-{self.low_freq_period}: {self.freq_low[-1]}\n\t\tSMA-{self.high_freq_period}: {self.freq_high[-1]}."

        return f"{self.ticker} prices today are:\n\t\tSMA-{self.low_freq_period}: {self.freq_low[-1]}\n\t\tSMA-{self.high_freq_period}: {self.freq_high[-1]}."

    def report_streak(self) -> str:
        """

        The self.status refers to relative price of lower frequency SMA (e.g. 3) relative to higher frequency SMA (e.g. 10).

        If 3-SMA is lower than 10-SMA, it means that prices are currently going down.

        """

        self.alert_message = f"Low freq price is currently {self.status}, at {self.freq_low[-1]} compared to high freq price {self.freq_high[-1]}."
        self.duration_message = f"Current status has been ongoing for \
                                {self.status_duration} days."

        if self.status == "lower" and \
            self.prev_status == "higher" and \
                self.status_duration >= self.low_streak_alert:

            self.buy_message = f"Status duration has passed {self.low_streak_alert}. Consider buying!"

            self.logs.logger.info(f"Today's message: {self.alert_message}\n{self.duration_message}\n{self.buy_message}")
            return f"{self.alert_message}\n{self.duration_message}\n{self.buy_message}"

        if self.status == "higher" and \
            self.prev_status == "lower" and \
                self.status_duration >= self.high_streak_alert:

            self.sell_message = f"Status duration has passed {self.low_streak_alert}. Consider selling!"


            self.logs.logger.info(f"Today's message: {self.alert_message}\n{self.duration_message}\n{self.sell_message}")
            return f"{self.alert_message}\n{self.duration_message}\n{self.sell_message}"

        self.logs.logger.info(f"Returning: Status is {self.status}.\nPrevious status is{self.prev_status}.\nCurrent status duration is {self.status_duration}")
        return f"Status is {self.status}.\nPrevious status is{self.prev_status}.\nCurrent status duration is {self.status_duration}"

    def _save_raw_sma_json(self, time_period: int, storage: deque) -> bool:

        json_file = self._call_api(time_period)

        if json_file is None:
            self.logs.logger.warning(f"API call for {self.ticker} returned none.")
            return False

        self._store_raw_json(
            storage,
            json_file
        )
        self._write_to_txt(time_period, json_file)

        return True

    def _store_raw_json(self, storage_deque: deque, json_file: JSONType) -> None:

        base = dt.datetime.today()

        date_list = [base - dt.timedelta(days=x) for x in range(self.days_to_store)]
        date_list: List[str] = [date.strftime(self.date_format) for date in date_list]
        print(f"earliest date is {date_list[-1]}")

        idx = 0
        for date in date_list[::-1]:
            try:
                storage_deque.append(json_file[JSON_KEY][date][self.function]) # type: ignore
            except KeyError:
                self.logs.logger.info(f"{self.ticker}: {date} contains no information. Utilising price from previous available data.")
                print(f"{self.ticker}: {date} contains no information. Utilising price from previous available data.")
                if idx == 0:
                    self.logs.logger.info(f"idx is {idx}, we need to go back further in time.")
                    print(f"idx is {idx}, we need to go back further in time.")
                    found_price = False

                    go_back = 1
                    while not found_price:
                        curr_d = dt.datetime.strptime(date, self.date_format)
                        back_d = curr_d - dt.timedelta(days=go_back)
                        d = back_d.strftime(self.date_format)
                        print(f"date is {d}")
                        try:
                            storage_deque.append(json_file[JSON_KEY][d][self.function]) # type: ignore
                            self.logs.logger.info(f"found first price at {d}")
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

        self.logs.logger.info(f"Stored {self.ticker} prices in deque.")

    def _call_api(self, time_period: int) -> JSONType:
        api_call = f"{BASE_URL}{FUNCTION}={self.function}&{SYMBOL}={self.ticker}&{INTERVAL}={self.interval}&{TIME_PERIOD}={time_period}&{SERIES_TYPE}={self.series_type}&{APIKEY}={vintage_api_key}"

        res = requests.get(api_call)

        if res.status_code != 200:
            self.logs.logger.error(f"API call returned not 200 status code.\nReturned status code {res.status_code}")
            raise ValueError(f"API call returned not 200 status code.\nReturned status code {res.status_code}")

        if JSON_KEY not in res.json().keys():
            self.logs.logger.error(f"API call returned status 200 but did not retrieve the information prices. \nReturned product is {res.json()}")
            print(f"API call returned status 200 but did not retrieve the information prices. \nReturned product is {res.json()}")
            return None

        return res.json()

    def _write_to_txt(self, time_period: int, json_file: JSONType) -> None:
        with open(f"{self.file_path}_{time_period}.txt", "w") as f:
            for k, v in json_file[JSON_KEY].items(): # type: ignore
                f.write(f"{k} ")
                f.write(f"{json_file[JSON_KEY][k][self.function]}\n") # type: ignore

        self.logs.logger.info(f"Successfully saved {self.ticker} information to json.")

    def _update_price_in_txt(
        self,
        date: str,
        storage: deque,
        time_period: int) -> None:

        with open(f"{self.file_path}_{time_period}.txt", "r") as f:
            curr = f.read()
        with open(f"{self.file_path}_{time_period}.txt", "w") as f:
            f.write(f"{date} {storage[-1]}")
            f.write(curr)

        self.logs.logger.info(f"Successfully updated {self.ticker} price to json.")

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

        if self.prev_status is None:
            self.prev_status = self.status

        tmp_status = "lower" if self.freq_low[-1] < self.freq_high[-1] else "higher"

        if tmp_status != self.status:
            self.status_duration = 0
            self.prev_status = self.status
            self.status = tmp_status
        else:
            self.status_duration += 1

        self.logs.logger.info(f"Successfully updated {self.ticker} return status.")

    def _backup_var_to_json(self) -> None:

        freq_low_list: List[float] = []
        freq_high_list: List[float] = []

        idx = len(self.freq_low)
        while idx > 0:
            tmp = self.freq_low.popleft()
            freq_low_list.append(tmp)
            # rotate this all the way around again
            self.freq_low.append(tmp)
            idx -= 1

        idx2 = len(self.freq_high)
        while idx2 > 0:
            tmp2 = self.freq_high.popleft()
            freq_high_list.append(tmp2)
            self.freq_high.append(tmp2)
            idx2 -= 1

        backup: Dict[str, Any] = {

            "status_duration":   self.status_duration,
            "prev_status":       self.prev_status,

            "function":          self.function,
            "interval":          self.interval,
            "series_type":       self.series_type,
            "days_to_store":     self.days_to_store,

            "low_freq_period":   self.low_freq_period,
            "high_freq_period":  self.high_freq_period,
            "low_streak_alert":  self.low_streak_alert,
            "high_streak_alert": self.high_streak_alert,

            "freq_low":          freq_low_list,
            "freq_high":         freq_high_list,
            "date_format":       self.date_format,

            "save_path":         self.save_path,
            "file_path":         self.file_path
        }

        with open(f"./fund_backup/{self.ticker}.json", "w") as file:
            json.dump(backup, file)

        self.logs.logger.info(f"Successfully backed-up {self.ticker} information to json.")

    def restore_from_json(self, path) -> None:
        with open(path, "r") as file:
            restore = json.load(file)

        self.status_duration   = restore["status_duration"]
        self.prev_status       = restore["prev_status"]

        self.function          = restore["function"]
        self.interval          = restore["interval"]
        self.series_type       = restore["series_type"]
        self.days_to_store     = restore["days_to_store"]

        self.low_freq_period   = restore["low_freq_period"]
        self.high_freq_period  = restore["high_freq_period"]
        self.low_streak_alert  = restore["low_streak_alert"]
        self.high_streak_alert = restore["high_streak_alert"]

        self.date_format       = restore["date_format"]
        self.save_path         = restore["save_path"]
        self.file_path         = restore["file_path"]

        freq_low_list          = restore["freq_low"]
        freq_high_list         = restore["freq_high"]

        self.freq_low: Deque[float] = deque(maxlen=self.days_to_store)
        self.freq_high: Deque[float] = deque(maxlen=self.days_to_store)

        for price in freq_low_list:
            self.freq_low.append(price)
        for price in freq_high_list:
            self.freq_high.append(price)

        self.logs.logger.info(f"Successfully restored {self.ticker} information to json.")

if __name__ == "__main__":

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

    function = "SMA"
    interval = "daily"
    series_type = "close"
    days_to_store = 120
    low_freq_period = 3
    high_freq_period = 10
    low_streak_alert = 1
    high_streak_alert = 5
    save_path = "./data"

    ticker="AAPL"

    aapl_fund = fund(
        ticker=ticker,
        logs=LOGS
    )
    # print(aapl_fund.freq_low)

    aapl_fund.initial_build(
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

    # CANNOT slice a deque object
    # print(aapl_fund.freq_low[3:5])

    aapl_fund.update_price()
    time.sleep(3)
    aapl_fund.update_price()

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