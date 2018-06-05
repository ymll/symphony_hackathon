
# coding: utf-8
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.text import Text
import pandas as pd

keyWorks = [
	'price',
	'compare',
	'vwap'
]

routingPaths = [
	'/stock/<stockname>',
	'/compare/<stocka>/<stockb>',
	'/vwap/<stockname>'
]

stockNameSymbols = {
	'apple': 'AAPL',
	'google': 'GOOG',
	'goldman sachs': 'GS',
	'morgan stanley': 'MS'
}

class Parser:	
	dfStock = []
	def __init__(self):
		dfStock = pd.read_csv('data/constituents.csv')

	def getParseResult(self, question):
		tokens = word_tokenize(question);
		path = self.getRoutingPath(tokens)
		stockNames = self.getStockNames(tokens)
		parameter = {
			'StockNames': stockNames
		}
		return (path, parameter)

	def getRoutingPath(self, tokens):
		for i, v in enumerate(tokens):
			if v in keyWorks:
				print(v, 'index ', i)
				return routingPaths[i]
		return None

	def getStockNames(self, tokens):
		results = []
		for t in tokens:
			if t in stockNameSymbols:
				results.append(stockNameSymbols[t])
		return results
