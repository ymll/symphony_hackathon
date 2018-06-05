
# coding: utf-8
from flask import request
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.text import Text
from router import Router
from datetime import datetime, timedelta

router = Router()
today = datetime.now()

class Parser:
	def parseDate(strDate, defaultDate):
	    result = defaultDate
	    if strDate != None:
	        result = datetime.strptime(strDate, "%Y-%m-%d")
	    return(result)

	def getStockNames(self):
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

		start = parseDate(request.args.get('start'),today-timedelta(days=5*365))
		end = parseDate(request.args.get('end'),today)

		sentence = b; #enter command here
		tokens = word_tokenize(sentence);
		textList = Text(tokens)
		print (textList)

		results = [];
		for word in tokens:
			if word in stocks:
				results.append(word);

		print (results)
		length = len(results)

		if length == 1:
		    print ('one stock')
		    Router.getStockNames(results[0], start, end)

		if length == 2:
		    print ('two stocks')
		
		return results
