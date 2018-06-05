
# coding: utf-8
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.text import Text


routingPaths = [
	'/stock/<stockname>',
	'/compare/<stocka>/<stockb>',
	'/vwap/<stockname>'
]

class Parser:	
	def getRoutingPath(self, question):
		path = routingPaths[0]
		paramemter = ['AAPL']
		return((path, paramemter))
		
	def getStockNames(self, question):
		a = "What is the market colour for google?"
		b = "What is market color for GOOGL?"
		c = "market color GOOGL?"
		d = "How are apple and tesla doing?"
		e = "How are APPL and TESL doing?"

		stocks = [
		    'APPL',
		    'apple',
		    'GOOGL',
		    'google'
		]

		sentence = question; #enter command here
		tokens = word_tokenize(sentence);
		textList = Text(tokens)
		print (textList)

		results = [];
		for word in tokens:
			if word in stocks:
				results.append(word);
		print (results)
		
		return results
