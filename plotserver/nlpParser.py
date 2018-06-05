
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
		stocksInSentence = self.getStockNames(question);
		VWAPInSentence = self.getVWAP(question);
		length = len(stocksInSentence);
		if length == 1:
			if VWAPInSentence == True:
				path = routingPaths[2]
			else:
				path = routingPaths[0]
			paramemter = stocksInSentence[0]
		if length == 2:
			path = routingPaths[2]
			paramemter = stocksInSentence
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
		    'GOOG',
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
		
		return [results]

	def getVWAP(self, question):
		vwapVariables = [
			'vwap'
			'volume'
		]

		sentence = question; #enter command here
		tokens = word_tokenize(sentence);
		textList = Text(tokens)

		vwap = False;
		for word in tokens:
			if word in vwapVariables:
				vwap = True;
		
		return vwap
