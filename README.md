## Table of Contents

- [Introduction](#introduction)
- [Alpha Vantage](#alpha-vantage)
- [Initial Setup](#initial-setup)
- [Virtual Env](#virtual-env)
- [Docker](#docker)
- [Makefile](#makefile)
- [Type Hinting](#type-hinting)
- [SQLite3](#sqlite3)
- [Logging](#logging)
- [Adding Tickers](#adding-tickers)
- [Worklog](#work-log)

---

## Introduction

The `ETF Tracker` project takes a list of funds that we're interested in and returns past price movements.

The idea is simple, we are not waiting for a huge dip, but make regularly investments guided by slight dips in price.

The hypothesis is that we can squeeze in slightly more returns.

## Alpha Vantage

The API we use to retrieve information will be Alpha Vantage. There's a Python library, but for portability we can write it as API calls.

The free API key allows for roughly 5 calls/min, limited to a total of 500 calls/day.

Put the VANTAGE_API_KEY as an environment variable with
```
export VANTAGE_API_KEY=$(cat VANTAGE_API_KEY)
```
and retrieve it with
```{python}
vantage_api_key = os.environ.get('VANTAGE_API_KEY')

if vantage_api_key is None:
    raise ValueError("vantage_api_key not set as environment variable!")
```
Note: Exporting of environment variables must be done in the same shell process.

## ASX Tickers

Returning ASX tickers e.g. IOZ.AX is unreliable, sometimes it works and sometimes it doesn't. This interface will be built and tested with US equities for ease of testing.

See [here](http://gnucash.1415818.n4.nabble.com/Finance-Quote-ASX-problems-alphavantage-and-ASX-sources-td4697091.html) for a quick reference.

## Initial Setup

Test the script by running

```{bash}
python3 fund_package/main.py
```
The script will terminate if any of the tickers cannot be found, and return such a list.

## Virtual Env

To create a virtual environment:

```{python}
virtualenv venv
```

To activate and deactivate
```{bash}
source venv/bin/activate
```
```{bash}
deactivate
```

To record and install the modules in the Virtual Environment
```{bash}
pip3 freeze > requirements.txt

pip3 install -r requirements.txt
```

## Docker

First you have to download Docker [here](https://docs.docker.com/docker-for-mac/install/) (Mac) and install it.

Pulling the official Python image is straightforward

```{bash}

docker pull python:<version>
docker run -it python:<version> /bin/bash

docker run -d -p 80:80 --name <running_container_name> <image_name>

docker
```

Miscellaneous commands include

```{bash}
docker image ls
docker ps
docker top
```

## Type Hinting

Here are some references:
- [Code TutsPlus: Comprehensive guide](https://code.tutsplus.com/tutorials/python-3-type-hints-and-static-analysis--cms-25731)
- [RealPython Type Checking Guide](https://realpython.com/python-type-checking/)
- [Official Docs](https://docs.python.org/3.7/library/typing.html)

Some snippets:
- [Type hinting for JSON files](https://www.notion.so/jerryyexu/How-to-type-hint-for-JSON-files-05ced2e7b5394ddc87ea174ab14fec34#fd599f70941e4a3ba3766deb483f499e)

## SQLite3

When working with dates, use `BETWEEN` and wrap the `datetime` object in single quotation marks.

```{python}
import datetime as dt
import sqlite3

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cutoff_date = dt.datetime.today() - dt.timedelta(days=15)
today = dt.datetime.today().date()
cutoff_date = cutoff_date.date()

cur.execute(
    f"SELECT * FROM table_name WHERE date BETWEEN '{cutoff_date}' AND '{today}'; """
)

res = cur.fetchall()
```

To check all your tables in SQLite
```{sql}
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
res = cur.fetchall()
for r in res:
    print(r['name'])
```
In general, the table names are `<app_name>_<model_name>`. E.g. we will have `tracker_fund` and `tracker_fundprices`, which is consistent.

To view columns of a table
```
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
res = cur.fetchall()
for r in res:
    print(r['name']) # You can get list of key-value pairs with r.keys()
```

## Using Mypy

__Full version__

```{bash}
mypy --ignore-missing-imports --allow-redefinition ./src/fund_sma.py ./src/main.py ./src/logging_obj.py
```

__Quick guide__

To run mypy on a python file, simply install it and
```{bash}
mypy <file.py>
```

To ignore import errors of the type add the `-ignore-missing-imports` flag.

```{bash}
mypy --ignore-missing-imports ./fund_package/fund_sma.py
```

To ignore an error add a comment like below
```{python}
def func(x: str) -> None:
    y = None
    y = x # type: ignore
```

To allow for re-defintions add the following flag
```{python}
mypy --allow-redefinition ./src/fund_sma.py
```
The PR is [here](https://github.com/python/mypy/pull/6197) and the original Github issue is [here](https://github.com/python/mypy/issues/1174)

## Logging

To specify a `streamHandler` explicitly, you can simply
```{python}
sh = logging.StreamHandler(sys.stdout) # sys.stderr etc.
```
For more and adding filters see [here](https://stackoverflow.com/questions/1383254/logging-streamhandler-and-standard-streams)

## Adding Tickers

Different exchanges have different abbreviations. For the ASX, it is "AX" and thus the iShares ASX200 would be "IOZ.AX"

For more information check out this repo [here](https://github.com/prediqtiv/alpha-vantage-cookbook)

The list of ETFs traded on the ASX can be found [here](https://www.marketindex.com.au/asx-etfs#aust-broad-exposure)

## Worklog

- 0.0.13-rc | 17/02/20: Finished first prototype of d3 chart. Minimal but we have made something appear.
- 0.0.12-rc | 16/02/20: Build pagination, add additional fund data with migration. Add `latest_low/high_price` to `fund.py`.
- 0.0.11-rc | 19/01/20: Add links, about page, hover for dropdown, links to tickers, `json_script` for passing data to d3js.
- 0.0.10-rc | 18/01/20: Moved Bulma to actual html templates not just `bulma_testing.html`. Sorted out the `MEDIA_URL` and `MEDIA_ROOT` issue.
- 0.0.09-rc | 18/01/20: Changed CSS to Bulma. Built `fund_daily_update.py` that directly updates the DB.
- 0.0.08-rc | 12/01/20: Added `views` to display data on webpage for `ListView`.
- 0.0.07-rc | 12/01/20: Add Django backend with models and initial database schema and data migrations. Allow for `fund_package` to be an installable package within the Django backend.
- 0.0.06-rc | 11/01/20: Add logging to `fund_sma.py`. Fix issues with `main.py`, you have to retrieve fund by indexing and not `for f in ALL_FUNDS` etc.
- 0.0.05-rc | 30/12/19: Add `mypy` checks, mostly done except the unresolved issue documented. Added backup and restoring of class variables.
- 0.0.04-rc | 25/12/19: Added checks for API calls, and return `False` if call fails. Tested `main.py` function.
- 0.0.03-rc | 23/12/19: Added `run_daily_update()` to `fund_sma.py`. Implement the function indefinitely in the `main.py` function. Refactored some functions.
- 0.0.02-rc | 22/12/19: Re-wrote storage and retrieval for SMA prices instead of daily prices. Ensure an empty object is returned if API call limit is reached.
- 0.0.01-rc | 08/12/19: Confirmed API key, setup `fund` object for daily prices.
