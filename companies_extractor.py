import pandas as pd

class static_companies_extractor:

	def __init__(self, my_companies):
		self.__my_companies = my_companies

	def get_companies_list(self, current_portfolio = None):
		return pd.DataFrame({'Ticker':self.__my_companies})