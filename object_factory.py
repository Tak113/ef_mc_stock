# price_extractor.py
from price_extractor import price_extractor
# calculator.py
from calculator import metrics_calculator
# chart_plotter.py
from chart_plotter import chart_plotter
# optimiser_factory.py
import optimiser_factory as optimiser_factory
# monte carlo simulator.py
from monte_carlo_simulator import monte_carlo_simulator

class object_factory:
	#initialize the attributes of the class
	def __init__(self, settings):
		self.__settings = settings

	#pull stock price for each ticker
	def get_price_extractor(self, companies):
		return price_extractor(self.__settings.API, companies)

	def get_metrics_calculator(self):
		return metrics_calculator

	# create charts for the stock over horizon
	# this self is from get_metrics_calculator
	def get_charts_plotter(self):
		return chart_plotter(self.get_metrics_calculator)

	# optimisation
	def get_optimiser(self, targets, size):
		return optimiser_factory.optimiser(self.get_metrics_calculator(),
			self.__settings.RiskFunction, self.__settings.ReturnFunction,
			targets, size)
	
	# random portfolio prediction
	def get_portfolio_generator(self):
		return monte_carlo_simulator(self.get_metrics_calculator(), self.__settings.RiskFunction,
			self.__settings.ReturnFunction)