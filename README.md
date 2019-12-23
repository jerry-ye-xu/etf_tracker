## Table of Contents

- [Introduction](#introduction)
- [Alpha Vantage](#alpha-vantage)
- [Initial Setup](#initial-setup)
- [Virtual Env](#virtual-env)
- [Type Hinting](#type-hinting)

---

## Introduction

The `ETF Tracker` project takes a list of funds that we're interested in and returns past price movements.

The idea is simple, we are not waiting for a huge dip, but make regularly investments guided by slight dips in price.

The hypothesis is that we can squeeze in more returns.

## Alpha Vantage

The API we use to retrieve information will be Alpha Vantage. There's a Python library, but for portability we can write it as API calls.

The free API key allows for roughly 5 calls/min, limited to a total of 500 calls/day.

## Initial Setup



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

## Type Hinting



## Worklog

- 0.0.2-rc | 22/12/19: Re-wrote storage and retrieval for SMA prices instead of daily prices. Ensure an empty object is returned if API call limit is reached.
- 0.0.1-rc | 08/12/19: Confirmed API key, setup `fund` object for daily prices.