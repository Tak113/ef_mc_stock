# import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class chart_plotter:

	def __init__(self, mc):
		self.__mc = mc

	# stock price plot
	def plot_prices(self, closing_prices):
		#'Date' is not in column but time series, and plotly automatically read so no need to set x axis
		df = pd.DataFrame(closing_prices)
		fig = px.line(
			df,
			y=df.columns,
			title = 'Stock Price',
		)
		fig.update_layout(
			template='plotly_dark',
			yaxis_tickprefix = '$',
			legend_title_text = 'Ticker'
		)
		fig.update_xaxes(title='Time Horizon')
		fig.update_yaxes(title='Stock Prices $')
		fig.show()
		# print(df.columns)

	# stock daily changes plot
	def plot_returns(self, returns):
		df = pd.DataFrame(returns)
		fig = px.line(
			df,
			y=df.columns,
			title = 'Stock Price Daily Changes',
		)
		fig.update_layout(
			template = 'plotly_dark',
			legend_title_text = 'Ticker'
		)
		fig.update_xaxes(title= 'Time Horizon')
		fig.update_yaxes(
			title='Daily Changes %',
			tickformat = ',.0%'
		)
		fig.show()

	# correlation matric using daily change rate across stocks
	def plot_correlation_scatter(self, returns):
		df = pd.DataFrame(returns)
		fig = px.scatter_matrix(
			df,
			title = 'Daily Changes Correlation'
		)
		fig.update_layout(
			template = 'plotly_dark'
		)
		fig.show()

	# correlation matric using daily change rate across stocks
	def plot_correlation_matrix(self, returns):
		df = returns.corr()
		fig = px.imshow(
			df,
			labels = dict(
					color = 'Correlation Coefficiency'
			),
			title = 'Daily Changes Correlation Matrix'
		)
		fig.update_layout(
			template = 'plotly_dark'
		)
		fig.show()

	# horizontal bar chart for expected returns
	def plot_expected_returns(self, expected_returns):
		df = pd.DataFrame(expected_returns)
		fig = px.bar(
			df,
			orientation = 'h',
			title = 'Annual Expected Returns (mean of daily returns * 252 annual ops days)'
		)
		fig.update_xaxes(
			title = 'Expected Returns %',
			tickformat = ',.0%'
		)
		fig.update_yaxes(title = 'Ticker')
		fig.update_layout(
			template = 'plotly_dark',
			yaxis = {'categoryorder':'total ascending'},
			showlegend=False,
		)
		fig.show()

	# howizontal bar chart for cagr
	def plot_cum_daily_return(self, cum_return):
		df = pd.DataFrame(cum_return)
		fig = px.line(
			df,
			y=df.columns,
			title = 'Cumulative Stock Price against 1$ investment',
		)
		fig.update_layout(
			template = 'plotly_dark',
			yaxis_tickprefix = '$',
			legend_title_text = 'Ticker'
		)
		fig.update_xaxes(title = 'Time Horizon')
		fig.update_yaxes(
			title = 'Stock Prices $',
			tick0=0,
			dtick=1,
		)
		fig.show()

	# efficient frontier plot
	def plot_efficient_frontier(self, portfolio_risk_return_ratio_df, min_risk, max_sr):
		df = pd.DataFrame(portfolio_risk_return_ratio_df)

		# EF curve
		EF_curve = go.Scatter(
			name = 'Efficient Frontier',
			mode = 'lines',
			x = df['Risk'],
			y = df['Return'],
		)
		
		# max sharp ratio
		MaxSharpeRatio = go.Scatter(
			name = 'Maximum Sharpe Ratio',
			mode = 'markers',
			x = [max_sr.Risk],
			y = [max_sr.Return],
			marker = dict(color = 'indianred', size = 10),
		)

		# min risk
		MinVol = go.Scatter(
			name = 'Minimum Volatility',
			mode = 'markers',
			x = [min_risk.Risk],
			y = [min_risk.Return],
			marker = dict(color = 'steelblue', size = 10),
		)

		data = [EF_curve, MaxSharpeRatio, MinVol]

		layout = go.Layout(
			title = 'Portfolio Optimization with Efficient Frontier',
			yaxis = dict(title = 'Annualised Return (%)'),
			xaxis = dict(title = 'Annualised Volatility : Std Dev (%)'),
		)

		fig = go.Figure(data = data, layout = layout)

		fig.update_layout(
			template = 'plotly_dark'
		)
		fig.show()

	# pie chart
	def plot_pie(self, max_sr, min_risk):
		# max SR
		df_maxSR = pd.DataFrame(max_sr)
		df_maxSR = df_maxSR.drop(index = ['Risk', 'Return', 'SharpeRatio'], axis = 0)
		labels_maxSR = df_maxSR.index.values.tolist()
		values_maxSR = df_maxSR.values.flatten().tolist()
		data_maxSR = {
			'values': values_maxSR,
			'labels': labels_maxSR,
			'domain': {'column': 0},
			'name': 'maxSR',
			# 'hoverinfo': 'label+percent+name',
			'hole': .4,
			'type': 'pie',
		}

		# min Vol
		df_minVol = pd.DataFrame(min_risk)
		df_minVol = df_minVol.drop(index = ['Risk', 'Return', 'SharpeRatio'], axis = 0)
		labels_minVol = df_minVol.index.values.tolist()
		values_minVol = df_minVol.values.flatten().tolist()
		data_minVol = {
			'values': values_minVol,
			'labels': labels_minVol,
			'domain': {'column': 1},
			'name': 'minVol',
			# 'hoverinfo': 'label+percent+name',
			'hole': .4,
			'type': 'pie',
		}

		data = [data_maxSR, data_minVol]
		# print(data)
		layout = go.Layout(
			{
				'title': 'Optimum Portfolio : Maximum Sharpe Ratio and Minimum Risk',
				'grid': {'rows':1, 'columns':2},
				'annotations': [
					{
						'text': 'Max SR',
						'font': {
							'size': 16
						},
						'x': 0.2,
						'y': 0.5,
						'showarrow': False,
					},
					{
						'text': 'Min Risk',
						'font': {
							'size': 16
						},
						'x': 0.8,
						'y': 0.5,
						'showarrow': False,
					}
				]
			}
		)

		fig = go.Figure(data = data, layout = layout)
		fig.update_layout(
			template = 'plotly_dark',
		)
		fig.show()