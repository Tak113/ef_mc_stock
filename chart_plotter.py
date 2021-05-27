# import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import streamlit as st

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
			legend_title_text = 'Ticker',
			legend = dict(
				yanchor = 'top',
				y = 0.99,
				xanchor = 'left',
				x = 0.01,
			)
		)
		fig.update_xaxes(title='Time Horizon')
		fig.update_yaxes(title='Stock Prices $')
		# fig.show()
		# print(df.columns)
		st.plotly_chart(fig)

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
			legend_title_text = 'Ticker',
			legend = dict(
				yanchor = 'top',
				y = 0.99,
				xanchor = 'left',
				x = 0.01,
			)
		)
		fig.update_xaxes(title= 'Time Horizon')
		fig.update_yaxes(
			title='Daily Changes %',
			tickformat = ',.0%'
		)
		# fig.show()
		st.plotly_chart(fig)

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
		# fig.show()
		st.plotly_chart(fig)

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
		# fig.show()
		st.plotly_chart(fig)

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
		# fig.show()
		st.plotly_chart(fig)

	# cumulatice chart
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
			legend_title_text = 'Ticker',
			legend = dict(
				yanchor = 'top',
				y = 0.99,
				xanchor = 'left',
				x = 0.01,
			)
		)
		fig.update_xaxes(title = 'Time Horizon')
		fig.update_yaxes(
			title = 'Stock Prices $',
			tick0=0,
			dtick=1,
		)
		# fig.show()
		st.plotly_chart(fig)

	# efficient frontier plot
	def plot_efficient_frontier(self, portfolio_risk_return_ratio_df, min_risk, max_sr, max_return, min_return, portfolio_risk_return_mc_df):
		op_df = pd.DataFrame(portfolio_risk_return_ratio_df)
		mc_df = pd.DataFrame(portfolio_risk_return_mc_df)

		# EF curve
		EF_curve = go.Scatter(
			name = 'Efficient Frontier',
			mode = 'lines',
			x = op_df['Risk'],
			y = op_df['Return'],
		)

		# max sharp ratio
		MaxSharpeRatio = go.Scatter(
			name = 'Max Sharpe Ratio',
			mode = 'markers',
			x = [max_sr.Risk],
			y = [max_sr.Return],
			marker = dict(color = 'darkseagreen', size = 12),
		)

		# min risk
		MinVol = go.Scatter(
			name = 'Min Volatility',
			mode = 'markers',
			x = [min_risk.Risk],
			y = [min_risk.Return],
			marker = dict(color = 'darkkhaki', size = 12),
		)

		# max return
		MaxReturn = go.Scatter(
			name = 'Max Return',
			mode = 'markers',
			x = [max_return.Risk],
			y = [max_return.Return],
			marker = dict(color = 'indianred', size = 12),
		)

		# min return
		MinReturn = go.Scatter(
			name = 'Min Return',
			mode = 'markers',
			x = [min_return.Risk],
			y = [min_return.Return],
			marker = dict(color = 'steelblue', size = 12),
		)

		# monte carlo random
		MC_random = go.Scatter(
			name = 'Random ' + str(len(mc_df)) + ' portfolio',
			mode = 'markers',
			x = mc_df['Risk'],
			y = mc_df['Return'],
			marker = dict(
				color = 'gray',
				size = 8,
				line = dict(
					color = 'white',
					width = 1,
				)
			),
			opacity = 0.5
		)

		# equal allocation (formula is in monte carlo sim)
		equal_allocations_portfolio = mc_df.loc[mc_df['Portfolio'] == 'EqualAllocationPortfolio']
		EqAllc = go.Scatter(
			name = 'Equal Allocation',
			mode = 'markers',
			x = equal_allocations_portfolio['Risk'],
			y = equal_allocations_portfolio['Return'],
			marker = dict(color = 'pink', size = 12)
		)

		data = [EF_curve, MaxSharpeRatio, MinVol, MaxReturn, MinReturn, MC_random, EqAllc]

		layout = go.Layout(
			title = 'Portfolio Optimization with Efficient Frontier',
			yaxis = dict(title = 'Annualised Return (%)'),
			xaxis = dict(title = 'Annualised Volatility : Std Dev (%)'),
		)

		fig = go.Figure(data = data, layout = layout)

		fig.update_xaxes(tickformat = ',.0%')
		fig.update_yaxes(tickformat = ',.0%')
		fig.update_layout(
			template = 'plotly_dark',
			height = 500,
			legend = dict(
				yanchor = 'bottom',
				y = 0.01,
				xanchor = 'right',
				x = 0.99,
			)
		)
		# fig.show()
		st.plotly_chart(fig)

	# plot montecarlo result
	def plot_portfolios(self, df):
		max_sharpe_ratio = self.__mc.get_mac_shape

	# pie/donut chart
	def plot_pie(self, max_sr, min_risk, max_return, min_return):
		# max SR
		df_maxSR = pd.DataFrame(max_sr)
		df_maxSR = df_maxSR.drop(index = ['Risk', 'Return', 'SharpeRatio'], axis = 0)
		labels_maxSR = df_maxSR.index.values.tolist()
		values_maxSR = df_maxSR.values.flatten().tolist()
		values_maxSR = [round(num, 3) for num in values_maxSR]
		data_maxSR = {
			'values': values_maxSR,
			'labels': labels_maxSR,
			'domain': {'column': 0, 'row': 0},
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
		values_minVol = [round(num, 3) for num in values_minVol]
		data_minVol = {
			'values': values_minVol,
			'labels': labels_minVol,
			'domain': {'column': 1, 'row': 0},
			'name': 'minVol',
			# 'hoverinfo': 'label+percent+name',
			'hole': .4,
			'type': 'pie',
		}

		# max return
		df_maxReturn = pd.DataFrame(max_return)
		df_maxReturn = df_maxReturn.drop(index = ['Risk', 'Return', 'SharpeRatio'], axis = 0)
		labels_maxReturn = df_maxReturn.index.values.tolist()
		values_maxReturn = df_maxReturn.values.flatten().tolist()
		values_maxReturn = [round(num, 3) for num in values_maxReturn]
		data_maxReturn = {
			'values': values_maxReturn,
			'labels': labels_maxReturn,
			'domain': {'column': 0, 'row': 1},
			'name': 'maxReturn',
			'hole': .4,
			'type': 'pie',
		}

		# min return
		df_minReturn = pd.DataFrame(min_return)
		df_minReturn = df_minReturn.drop(index = ['Risk', 'Return', 'SharpeRatio'], axis = 0)
		labels_minReturn = df_minReturn.index.values.tolist()
		values_minReturn = df_minReturn.values.flatten().tolist()
		values_minReturn = [round(num, 3) for num in values_minReturn]
		data_minReturn = {
			'values': values_minReturn,
			'labels': labels_minReturn,
			'domain': {'column': 1, 'row': 1},
			'name': 'minReturn',
			'hole': .4,
			'type': 'pie',
		}

		data = [data_maxSR, data_minVol, data_maxReturn, data_minReturn]
		# print(data)
		layout = go.Layout(
			{
				'title': 'Optimum Portfolio : 4 corner cases',
				'grid': {'rows':2, 'columns':2},
				'annotations': [
					{
						'text': 'Max SR',
						'font': {
							'size': 16
						},
						'x': 0.18,
						'y': 0.78,
						'showarrow': False,
					},
					{
						'text': 'Min Risk',
						'font': {
							'size': 16
						},
						'x': 0.82,
						'y': 0.78,
						'showarrow': False,
					},
					{
						'text': 'Max Return',
						'font': {
							'size': 16
						},
						'x': 0.16,
						'y': 0.22,
						'showarrow': False,
					},
					{
						'text': 'Min Return',
						'font': {
							'size': 16
						},
						'x': 0.84,
						'y': 0.22,
						'showarrow': False,
					}
				]
			}
		)

		fig = go.Figure(data = data, layout = layout)
		fig.update_layout(
			template = 'plotly_dark',
			height = 800,
		)
		# fig.show()
		st.plotly_chart(fig)
