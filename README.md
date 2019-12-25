## Table of Contents

- [Introduction](#introduction)
- [Alpha Vantage](#alpha-vantage)
- [Initial Setup](#initial-setup)
- [Virtual Env](#virtual-env)
- [Docker](#docker)
- [Makefile](#makefile)
- [Type Hinting](#type-hinting)
- [Worklog](#work-log)

---

## Introduction

The `ETF Tracker` project takes a list of funds that we're interested in and returns past price movements.

The idea is simple, we are not waiting for a huge dip, but make regularly investments guided by slight dips in price.

The hypothesis is that we can squeeze in slightly more returns.

## Alpha Vantage

The API we use to retrieve information will be Alpha Vantage. There's a Python library, but for portability we can write it as API calls.

The free API key allows for roughly 5 calls/min, limited to a total of 500 calls/day.

## Initial Setup

Test the script by running

```{bash}
python3 src/main.py
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

## Makefile



## Type Hinting

Here are some references:
- [Code TutsPlus: Comprehensive guide](https://code.tutsplus.com/tutorials/python-3-type-hints-and-static-analysis--cms-25731)
- [RealPython Type Checking Guide](https://realpython.com/python-type-checking/)
- [Official Docs](https://docs.python.org/3.7/library/typing.html)

Some snippets:
- [Type hinting for JSON files](https://www.notion.so/jerryyexu/How-to-type-hint-for-JSON-files-05ced2e7b5394ddc87ea174ab14fec34#fd599f70941e4a3ba3766deb483f499e)

## Worklog

- 0.0.4-rc | 25/12/19: Added checks for API calls, and return `False` if call fails. Tested `main.py` function.
- 0.0.3-rc | 23/12/19: Added `run_daily_update()` to `fund_sma.py`. Implement the function indefinitely in the `main.py` function. Refactored some functions.
- 0.0.2-rc | 22/12/19: Re-wrote storage and retrieval for SMA prices instead of daily prices. Ensure an empty object is returned if API call limit is reached.
- 0.0.1-rc | 08/12/19: Confirmed API key, setup `fund` object for daily prices.