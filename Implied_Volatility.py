import math
import scipy.stats as st
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import stockquotes
import quandl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from BlackScholesMerton import BlackScholesModel
import os

quandl.ApiConfig.api_key = os.environ.get('JMxryiBcRV26o9r5q7uv')

GSPC = yf.Ticker('^GSPC')

expirations = GSPC.options

GSPC_opts = GSPC.option_chain(expirations[0])

GSPC_calls = GSPC_opts.calls

expiration_date = datetime.strptime(expirations[1],"%Y-%m-%d")
td = datetime.now()
strike = GSPC_calls['strike'][1]
print(strike)

SP500 = stockquotes.Stock("^GSPC")
stock_price = SP500.current_price

implied_vol = GSPC_calls['impliedVolatility'][1]

BSM = BlackScholesModel(expiration_date, td,stock_price,strike, implied_vol)

print(BSM.risk_free())


