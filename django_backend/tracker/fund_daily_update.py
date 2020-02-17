import datetime as dt
import logging
import os
import sqlite3
import time

from fund_sma import fund
from logging_obj import LoggerObject

APP_NAME = "tracker"
FUND_TABLE = "fund"
FUND_PRICES_TABLE = "fundprices"

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

if __name__ == "__main__":

    DB_PATH = "./db.sqlite3"
    TICKERS_FILE = "../data/tickers_to_track.csv"

    if not os.path.exists(DB_PATH):
        raise ValueError("db_path provided does not exist.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Used to update prices
    id_ticker_dict = {}

    with open(TICKERS_FILE, "r") as f:
        num_tickers = f.readline()
        print(f"num_tickers: {num_tickers}")
        ALL_FUNDS = [None]*int(num_tickers)
        idx = 0
        for line in f:
            arr = [x.strip() for x in line.split(sep=",")]

            ticker: str = arr[0]
            days_to_store = 60
            ALL_FUNDS[idx] = fund(ticker, days_to_store, LOGS)

            cur.execute(
                f"SELECT * FROM {APP_NAME}_{FUND_TABLE} WHERE ticker=?",
                (ALL_FUNDS[idx].ticker,)
            )
            result = cur.fetchone()

            ALL_FUNDS[idx].function = result["function"]
            ALL_FUNDS[idx].interval = result["interval"]
            ALL_FUNDS[idx].series_type = result["series_type"]
            ALL_FUNDS[idx].days_to_store = result["days_to_store"]

            ALL_FUNDS[idx].low_freq_period = result["low_freq_period"]
            ALL_FUNDS[idx].high_freq_period = result["high_freq_period"]
            ALL_FUNDS[idx].low_streak_alert = result["low_streak_alert"]
            ALL_FUNDS[idx].high_streak_alert = result["high_streak_alert"]

            ALL_FUNDS[idx].status = result["status"]
            ALL_FUNDS[idx].status_duration = result["status_duration"]
            ALL_FUNDS[idx].prev_status = result["prev_status"]
            ALL_FUNDS[idx].holiday = result["holiday"]

            ALL_FUNDS[idx].latest_low_price = result["latest_low_price"]
            ALL_FUNDS[idx].latest_high_price = result["latest_high_price"]
            ALL_FUNDS[idx].most_recent_date = result["most_recent_date"]

            id_ticker_dict[ALL_FUNDS[idx].ticker] = result["id"]

            fund_id = result["id"]
            cutoff_date = dt.datetime.today() - dt.timedelta(days=10)
            cutoff_date = cutoff_date.strftime("%Y-%m-%d")
            cur.execute(
                f"SELECT * FROM {APP_NAME}_{FUND_PRICES_TABLE} WHERE fund_id={fund_id} AND DATE > {cutoff_date}"""
            )

            price_result = cur.fetchall()

            all_dates = [dt.datetime.today() - dt.timedelta(days=i) for i in range(15)]
            for res in price_result:
                # print(res.keys())
                if res["freq_type"] == "high":
                    ALL_FUNDS[idx].freq_high.append(res["price"])
                else:
                    ALL_FUNDS[idx].freq_low.append(res["price"])
                ALL_FUNDS[idx].freq_dates.append(res["date"])
                # for k in res.keys():
                #     print(f"{k}: {res[k]}")
                # print("---------")

            idx += 1

    for i in range(len(ALL_FUNDS)):
        print(f"ALL_FUNDS[i]: {ALL_FUNDS[i]}")
        print(ALL_FUNDS[i].ticker)
        print(ALL_FUNDS[i].run_daily_update())
        print(ALL_FUNDS[i].report_fund_price())

        sql_fund = """UPDATE tracker_fund
                SET status=? ,
                    status_duration=? ,
                    prev_status=? ,
                    holiday=? ,
                    latest_low_price=? ,
                    latest_high_price=? ,
                    most_recent_date=?
                WHERE ticker=?"""
        values_fund = (
            ALL_FUNDS[i].status,
            ALL_FUNDS[i].status_duration,
            ALL_FUNDS[i].prev_status,
            ALL_FUNDS[i].holiday,
            ALL_FUNDS[i].latest_low_price,
            ALL_FUNDS[i].latest_high_price,
            ALL_FUNDS[i].most_recent_date,
            ALL_FUNDS[i].ticker
        )
        cur.execute(
            sql_fund, values_fund
        )

        fund_id = id_ticker_dict[ALL_FUNDS[i].ticker]

        fp_values = [
            ("low", ALL_FUNDS[i].most_recent_date, ALL_FUNDS[i].latest_low_price, fund_id),
            ("high", ALL_FUNDS[i].most_recent_date, ALL_FUNDS[i].latest_high_price, fund_id)
        ]


        sql_fp ="""INSERT INTO tracker_fundprices(freq_type, date, price, fund_id) VALUES (?, ?, ?, ?)"""

        try:
            cur.executemany(
                sql_fp, fp_values
            )
        except sqlite3.IntegrityError:
            print(f"sqlite3.IntegrityError: Price has already been added on {ALL_FUNDS[i].most_recent_date}, for {ALL_FUNDS[i].ticker}")

        print("sleeping for 60 seconds")
        time.sleep(60)
    conn.commit()
    cur.close()