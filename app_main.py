import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import numpy as np
import pandas as pd

from settings import settings
from object_factory import object_factory
from mappers import portfolios_allocation_mapper

####################################################
# side bar

st.sidebar.title('Portfolio Optimization')

st.sidebar.write('  ')

st.sidebar.write('The app pulls ticker data from yahoo finance API and simulates multiple portfolios options in terms of `expected annualized return and volatility %`')

st.sidebar.header('Input')

# one empty row
st.sidebar.write('  ')

ticker = st_tags_sidebar(
	label = 'Type Ticker :',
	text = 'Press enter to add more',
	value = ['INTC', 'AAPL', 'AMD', 'NVDA', 'TSM'],
	maxtags = 10,
)

# one empty row
st.sidebar.write('  ')
st.sidebar.header('Settings')

# date input
n_yrs = st.sidebar.slider(
	label = 'N of Years to Pull',
	min_value = 1,
	max_value = 10,
	value = 3,
	step = 1,
	help = 'Number of historical years that app pulls stock data from Yahoo Finance'
)

# one empty row
st.sidebar.write('  ')

# N of monte carlo
n_mc = st.sidebar.slider(
	label = 'N of Random Portfolio',
	min_value = 1000,
	max_value = 10000,
	value = 5000,
	step = 1000,
	help = 'Number of random portfolio by monte carlo simulation'
)

# one empty row
st.sidebar.write('  ')

# run button
button = st.sidebar.button(
	label = 'Run Simulation',
	help = 'test',

)

# side bar end
####################################################



if button:
	st.write('test')
else:
	st.write('aaaasa')

st.write(ticker)

# function lists
obj_factory = object_factory(settings)

# call functions
ce = obj_factory.get_companies_extractor()

companies = ce.get_companies_list()

price_extractor = obj_factory.get_price_extractor(companies)

st.write()