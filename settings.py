import numpy as np
import datetime as dt
import pandas as pd
# calculator.py
from calculator import risk_return_calculator

class settings:

	API = 'yahoo'
	PriceEvent = 'Adj Close' # choose from 'High', 'Low', 'Open', 'Close', 'Volume', or 'Adj Close'
	DailyAssetsReturnsFunction = risk_return_calculator.calculate_daily_asset_returns
	AssetsExpectedReturnsFunction = risk_return_calculator.calculate_assets_expectedreturns
	AssetsCovarianceFunction = risk_return_calculator.calculate_assets_covariance
	DailyAssetsCumulativeReturnsFunction = risk_return_calculator.calculate_cum_returns
	RiskFunction = risk_return_calculator.calculate_portfolio_risk
	ReturnFunction = risk_return_calculator.calculate_portfolio_expectedreturns
	RiskFreeRate = 0

	@staticmethod
	def get_end_date():
		return dt.date.today()

	@staticmethod
	def get_start_date(end_date, n_yrs):
		return end_date - dt.timedelta(days = n_yrs * 365)

	@staticmethod
	def get_my_targets():
		return np.arange(0, 1.5, 0.01)

	@staticmethod
	def get_companies_list(ticker):
		return pd.DataFrame({'Ticker':ticker})

