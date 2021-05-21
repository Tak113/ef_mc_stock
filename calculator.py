import numpy as np
from functools import reduce
import pandas as pd

class metrics_calculator:
	
	@staticmethod
	def calculate_sharpe_ratio(risk, returns, risk_free_rate):
		return (returns - risk_free_rate)/risk

	@staticmethod
	def get_max_sharpe_ratio(df):
		return df.loc[df['SharpeRatio'].astype(float).idxmax()]
		# return df.iloc[df['SharpeRatio'].astype(float).idxmax()]

	@staticmethod
	def get_min_risk(df):
		return df.loc[df['Risk'].astype(float).idxmin()]
		# return df.iloc[df['Risk'].astype(float).idxmin()]

	@staticmethod
	def get_max_return(df):
		return df.loc[df['Return'].astype(float).idxmax()]

	@staticmethod
	def get_min_return(df):
		return df.loc[df['Return'].astype(float).idxmin()]


class risk_return_calculator:
	# daily asset returns
	@staticmethod
	def calculate_daily_asset_returns(stock_prices):
		return stock_prices.pct_change()
		# return np.log(stock_prices / stock_prices.shift(1))
		# return stock_prices / stock_prices.shift(1)

	@staticmethod
	def calculate_assets_expectedreturns(returns):
		return returns.mean() * 252 # can be assigned whatever multiplier. 252 is # annual days for trading

	@staticmethod
	def calculate_assets_covariance(returns):
		return returns.cov() * 252

	@staticmethod
	def calculate_cum_returns(returns):
		return (returns +1).cumprod()

	@staticmethod
	def calculate_portfolio_expectedreturns(returns, allocations):
		return sum(returns * allocations)

	#reduce(np.dot, [a, b, c]) = (a * b) * c
	@staticmethod
	def calculate_portfolio_risk(allocations, cov):
		return np.sqrt(reduce(np.dot, [allocations, cov, allocations.T]))