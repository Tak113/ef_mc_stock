import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import numpy as np
import pandas as pd

from settings import settings
from object_factory import object_factory
from mappers import portfolios_allocation_mapper

# set page configurations, app title, favicon, layout (either wide or narrow), etc.
st.set_page_config(
	page_title='Portfolio Optimization',
)


####################################################
####################################################
# side bar

st.sidebar.title('Portfolio Optimization')

st.sidebar.write('  ')

st.sidebar.write('The app pulls ticker data from yahoo finance API and simulates multiple portfolios options in terms of `expected annualized return and volatility %`.')
st.sidebar.write('Press button to start simulation')

# form
with st.sidebar.form(key = 'input_form'):
	st.header('Input')
	
	# one empty row
	st.write('  ')
	
	ticker = st_tags(
		label = 'Type Ticker :',
		text = 'Press enter to add more',
		value = ['INTC', 'AAPL', 'AMD', 'NVDA', 'TSM'],
		maxtags = 10,
	)
	
	# one empty row
	st.write('  ')
	st.header('Settings')
	
	# date input
	n_yrs = st.slider(
		label = 'N of Years to Pull',
		min_value = 1,
		max_value = 10,
		value = 3,
		step = 1,
		help = 'Number of historical years that app pulls stock data from Yahoo Finance'
	)
	
	# one empty row
	st.write('  ')
	
	# N of monte carlo
	n_mc = st.slider(
		label = 'N of Random Portfolio',
		min_value = 1000,
		max_value = 10000,
		value = 1000,
		step = 1000,
		help = 'Number of random portfolio by monte carlo simulation'
	)
	
	# one empty row
	st.write('  ')
	
	# run button
	submit = st.form_submit_button('Run Simulation')

	st.write('  ')
	st.write('  ')

st.sidebar.markdown('''
	***  
	[datak.biz](https://datak.biz)  
	[git repo](https://github.com/Tak113/streamlit_ef_mc)
''')

# side bar end
####################################################
####################################################




####################################################
####################################################
# main graph

# run following script if form button is submitted
if submit:
	st.title('Optimization Dashboard')
	st.markdown('***')

	# function lists
	obj_factory = object_factory(settings)
	
	# call functions
	cp = obj_factory.get_charts_plotter() # get stock charts over given time horizon
	mc = obj_factory.get_metrics_calculator()
	mcs = obj_factory.get_portfolio_generator()
	
	# get companies list by dataframe
	companies = settings.get_companies_list(ticker)
	
	# initialize price extractor
	price_extractor = obj_factory.get_price_extractor(companies)
	
	# get company stock prices
	end_date = settings.get_end_date()
	start_date = settings.get_start_date(end_date, n_yrs)

	with st.spinner('...getting company info'):
		closing_prices = price_extractor.get_prices(settings.PriceEvent, start_date, end_date)
		
		# plot stock charts
		st.header('Exploretory Data Analysis')
		st.write('  ')
		with st.beta_expander('About Analysis'):
			st.write('Review historical stock performance as a start')
			st.write('Then translate to daily percent change to see magnitude of daily stock fluctuations')
			st.write('Normalize stock perfomance starting as $1, then apply daily changes with all time horizon cumulated to predict how much $ changes did $1 stock at start has been made at last in the horizon')
			st.write('From different cut of expected changes, using annual change %. Use 252 operation dayas/yr multiply by mean of daily percent changes')
			st.write('Correlation and covariance are importance factor to group up which stocks behaves similarly. From asset allocation perspectives, having similar behavial stocks does not mitigate risk while having non-correlated stocks mitigate volatility risks')

		cp.plot_prices(closing_prices)
		
		# calculate daily returns
		returns = settings.DailyAssetsReturnsFunction(closing_prices)
		cp.plot_returns(returns)
		
		# calculate expected retutnrs
		cum_return = settings.DailyAssetsCumulativeReturnsFunction(returns)
		cp.plot_cum_daily_return(cum_return)
		
		# calculate expected mean return from daily changes
		expected_returns = settings.AssetsExpectedReturnsFunction(returns)
		cp.plot_expected_returns(expected_returns)
		
		# calculate covariance for efficient edge quantification
		covariance = settings.AssetsCovarianceFunction(returns)

		# visualize daily retunrs correlation
		cp.plot_correlation_scatter(returns)
		
		# visualize daily change correlation matrix
		cp.plot_correlation_matrix(returns)
	
	# monte carlo
	with st.spinner(f'...simulating {n_mc} of random portfolio'):
		# use an optimiser
		targets = settings.get_my_targets()
		optimiser = obj_factory.get_optimiser(targets, len(expected_returns.index))
		portfolios_allocations_df = optimiser.generate_portfolios(expected_returns, covariance, settings.RiskFreeRate)
		portfolio_risk_return_ratio_df = portfolios_allocation_mapper.map_to_risk_return_ratios(portfolios_allocations_df)
		portfolio_risk_return_allc_ratio_df = portfolios_allocation_mapper.map_to_risk_return_allc_ratio(portfolios_allocations_df)
		min_risk = mc.get_min_risk(portfolio_risk_return_allc_ratio_df)
		max_sr = mc.get_max_sharpe_ratio(portfolio_risk_return_allc_ratio_df)
		max_return = mc.get_max_return(portfolio_risk_return_allc_ratio_df)
		min_return = mc.get_min_return(portfolio_risk_return_allc_ratio_df)
		
		portfolios_allocations_df = mcs.generate_portfolios(expected_returns, covariance, settings.RiskFreeRate, n_mc)
		portfolio_risk_return_mc_df = portfolios_allocation_mapper.map_to_risk_return_ratios(portfolios_allocations_df)
		
		st.markdown('***')
		st.header('Optimization and Monte Carlo Simulation')
		st.write('  ')
		with st.beta_expander('About Simulation'):
			st.write('For a given stocks, getting efficient frontier edge curve. The edges are made by most efficient allocation.')
			st.write('From efficient frontier curve, getting 4 unique optimum portfolios, which are maximum return, minimum return, minimum risk, and maximum sharpe ratio.')
			st.write('Sharpe ratio is an indicator to measure return efficiency against risk(volatility).')
			st.write('On top of that, random portfolios are generated to show where un-optimised portfolios are placed')

		# plot portfolio
		# with st.spinner('Getting optimum and random portfolio'):
		cp.plot_efficient_frontier(portfolio_risk_return_ratio_df, min_risk, max_sr, max_return, min_return, portfolio_risk_return_mc_df)
		
		# allocation for optimum portfolios
		cp.plot_pie(max_sr, min_risk, max_return, min_return)

else:
	st.header('Get Started')
	st.warning('Fill out inputs at left panel and run simulation to see optimum portfolio and simulated random portfolios')
	st.subheader('About Inputs')
	st.info('Type Ticker : Stocks to be simulated optimum stock allocations')
	st.info('Numer of Years to Pull : Time series historical stock demonstrated data to be used for a simulation')
	st.info('Number of Random Portfolio : Random portfolio to be generated by monte carlo simulation')

# main graph end
####################################################
####################################################