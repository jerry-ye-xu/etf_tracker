# Common Libraries
from collections import deque
import datetime as dt
import requests
import subprocess as sp
from typing import Any, Union, Dict, List, Sequence

# Python Wrapper/Github Repositories
from alpha_vantage import timeseries as ts

# Local Python files
from type_hint_objs import JSONType

key_byte_str = sp.run(["cat", "VINTAGE_API_KEY"], capture_output=True).stdout
vintage_api_key = str(key_byte_str, "utf-8")

# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=MSFT&outputsize=compact&apikey=demo

BASE_URL = "https://www.alphavantage.co/query?"
FUNCTION = "function="
SYMBOL = "symbol="
OUTPUTSIZE = "outputsize="
APIKEY = "apikey="

class fund(object):
    """
    Stores information regarding the equity for the last 60 days.

    Parameter:
    ticker: The ticker symbol of the
    dec_stk: The current decreasing streak of the equity
    dec_prev_stk: The previous decreasing streak of the equity
    inc_stk: The current increasing streak of the equity
    inc_prev_stk: The previous increasing streak of the equity

    historical_data: Previous (60) days of adjusted closing price data stored in queue-like data structure.
    """
    def __init__(self, ticker: str, days_to_store: int) -> None:
        self.ticker = ticker
        self.days_to_store = days_to_store

        self.dec_stk = 0
        self.dec_prev_stk = 0
        self.inc_stk = 0
        self.inc_prev_stk = 0

        self._today_json = {}
        # We use deque because it automatically "wraps around" when maxlen is reached.
        self.historical_data = deque(maxlen=days_to_store)

    def _get_raw_json(self, function: str, output_size: str) -> None:
        api_call = f"{BASE_URL}{FUNCTION}{function}&{SYMBOL}{self.ticker}&{OUTPUTSIZE}{output_size}&{APIKEY}{vintage_api_key}"

        res = requests.get(api_call)

        if res.status_code != 200:
            raise ValueError(f"API call was not successful.\nReturned status code {res.status_code}")

        self._today_json = res.json()

    def _process_raw_json(self) -> None:
        base = dt.datetime.today()
        date_format = "%Y-%m-%d"
        if len(self.historical_data) == 0:
            date_list = [base - dt.timedelta(days=x) for x in range(self.days_to_store) if not fund._check_if_weekday((base - dt.timedelta(days=x)))]

            for date in date_list:
                date_str = date.strftime(date_format)

                # Catch the holidays
                try:
                    self.historical_data.appendleft(self._today_json["Time Series (Daily)"][f"{date_str}"]["4. close"])
                except KeyError:
                    print(f"The market is closed today on {date_str}")

        else:
            date_str = base.strftime(date_format)
            try:
                self.historical_data.appendleft(self._today_json["Time Series (Daily)"][f"{date_str}"]["5. adjusted close"])
            except KeyError:
                    print(f"The market is closed today on {date_str}")

    def _compute_initial_streaks(self) -> None:
        item_idx = len(self.historical_data)
        hd_list = list(self.historical_data)

        curr_idx = item_idx - 1
        if hd_list[curr_idx] >= hd_list[curr_idx-1]:
            while curr_idx > 1:
                if (hd_list[curr_idx] > hd_list[curr_idx-1]):
                    self.inc_stk += 1

                    curr_idx -= 1
                else:
                    self.inc_prev_stk = self.inc_stk
                    self.inc_stk = 0

                    return
        else:
            while curr_idx > 1:
                if (hd_list[curr_idx] < hd_list[curr_idx-1]):
                    self.dec_stk += 1

                    curr_idx -= 1
                else:
                    self.dec_prev_stk = self.dec_stk
                    self.dec_stk = 0

                    return

    def _update_streak(self) -> None:
        idx = len(self.historical_data)

        if hd_list[curr_idx] >= hd_list[curr_idx-1]:
            self.inc_stk += 1
            if self.dec_stk > 0:
                self.dec_prev_stk = self.dec_stk
                self.dec_stk = 0
        else:
            self.dec_stk += 1
            if self.inc_stk > 0:
                self.inc_prev_stk = self.inc_stk
                self.inc_stk = 0

    def get_historical_data(self) -> deque:
        return self.historical_data

    def get_streaks(self) -> Dict:
        return {
            "dec_stk": self.dec_stk,
            "dec_prev_stk": self.dec_prev_stk,
            "inc_stk": self.inc_stk,
            "inc_prev_stk": self.inc_prev_stk
        }

    ####################################

    ######    HELPER FUNCTIONS    ######

    ####################################

    @staticmethod
    def _check_if_weekday(date: dt.datetime) -> bool:
        if date.weekday() == 5 or date.weekday() == 6:
            return True
        else:
            return False

if __name__ == "__main__":
    key_byte_str = sp.run(["cat", "VINTAGE_API_KEY"], capture_output=True).stdout

    api_key = str(key_byte_str, "utf-8")

    # ts = ts.TimeSeries(api_key, output_format="json")
    # aapl, meta = ts.get_daily_adjusted(
    #     symbol="AAPL",
    #     outputsize="compact"
    # )
    # print(aapl)

    aapl_fund = fund(ticker="AAPL", days_to_store=60)
    print(aapl_fund._today_json)
    json_file = aapl_fund._get_raw_json(
        function="TIME_SERIES_DAILY_ADJUSTED",
        output_size="compact"
    )
    aapl_fund._process_raw_json()

    aapl_fund._compute_initial_streaks()

    print(aapl_fund.get_streaks())


    # print(json_file)
    # print(json_file["Time Series (Daily)"]["2019-11-29"]["5. adjusted close"])

    def _check_if_weekday(date: dt.datetime) -> bool:
        if date.weekday() == 5 or date.weekday() == 6:
            return True
        else:
            return False

    base = dt.datetime.today()
    print(_check_if_weekday(base))

