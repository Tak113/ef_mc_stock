import pandas as pd

class portfolios_allocation_mapper:

	@staticmethod
	def map_to_risk_return_ratios(input):
		#remove 'Symbol' and 'MeanReturn' and start from 'Portfolio_1'
		portfolios = input.columns.values[2:]
		# filter return record
		returns = input.loc[input['Symbol'] == 'Return'].values[0][2:]
		# filter risk record
		risks = input.loc[input['Symbol'] == 'Risk'].values[0][2:]
		# filter sharpe ratio
		sharpe_ratios = input.loc[input['Symbol'] == 'SharpeRatio'].values[0][2:]

		df = pd.DataFrame(
			{
				'Portfolio': portfolios,
				'Return': returns,
				'Risk': risks,
				'SharpeRatio': sharpe_ratios
			}
		)

		return df
	# transpose 'portfolio_allocations_df' and remove 'MeanReturn' column
	@staticmethod
	def map_to_risk_return_allc_ratio(input):
		df = input.T
		df = df[2:]
		df.columns = input['Symbol']

		return df