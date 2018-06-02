from flask import Flask, request
from router import Router
from datetime import datetime, timedelta

router = Router()
today = datetime.now()

app = Flask(__name__)
app.debug = True

def parseDate(strDate, defaultDate):
    result = defaultDate
    if strDate != None:
        result = datetime.strptime(strDate, "%Y-%m-%d")
    return(result)

@app.route('/')
def index():
    return("welcome to symphony hackathon")

@app.route('/stock/<stockname>')
def apple(stockname):
    start = parseDate(request.args.get('start'),today-timedelta(days=5*365))
    end = parseDate(request.args.get('end'),today)
    return(router.getStock(stockname, start, end))

@app.route('/compare/<stocka>/<stockb>')
def compare(stocka, stockb):
    start = parseDate(request.args.get('start'),today-timedelta(days=5*365))
    end = parseDate(request.args.get('end'),today)
    return(router.compareStock(stocka, stockb, start, end))

@app.route('/vwap/<stockname>')
def vwap(stockname):
    start = parseDate(request.args.get('start'),today-timedelta(days=5*365))
    end = parseDate(request.args.get('end'),today)
    return(router.stockVWAP(stockname, start, end))


if __name__ == '__main__':
    app.run(host='0.0.0.0',  debug=True,  port=6312)