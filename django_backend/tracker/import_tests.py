import logging
import os
import subprocess as sp
import sys

print(sys.path)

import fund_sma

from fund_sma import fund
from logging_obj import LoggerObject

# vintage_api_key = str(key_byte_str, "utf-8")

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


