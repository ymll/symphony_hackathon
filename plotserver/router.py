import pandas_datareader as web
import plotly.graph_objs as go
import plotly.plotly as plt
from pathlib import Path
from flask import render_template
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as mplot
import statsmodels.api as sm
from statsmodels import regression


plt.sign_in('sheepjian', 'jpl9cET3s2Ytr8riYYJR') # Replace the username, and API key with your credentials.

imageFolder = "static"
stockChartBaseName = "-simple-plot.png"
stockTemplate = "stock.html"

def fileBaseName(startTime, endTime):
    return(startTime.strftime("%Y-%m-%d") + '-' \
            + endTime.strftime("%Y-%m-%d") + \
            "-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") +stockChartBaseName) 

def linReg(x,y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y,x).fit()
    x = x[:,1]
    return model.params[0], model.params[1]


class Router:
    def getStock(self, stockname, startTime, endTime):
        filename = stockname + "-" + fileBaseName(startTime, endTime)
        filePath = imageFolder +'/'  + filename

        # to be replaced by market data service
        df = web.DataReader(stockname, 'morningstar', startTime, endTime).reset_index()
        trace = go.Ohlc(x=df.Date,
                open=df.Open,
                high=df.High,
                low=df.Low,
                close=df.Close)

        layout = go.Layout(
            xaxis = dict(
                rangeslider = dict(
                    visible = False
                )
            )
        )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
        
        plt.image.save_as(fig, filename=Path(filePath))

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

    def compareStock(self, stocka, stockb, startTime, endTime):
        filename = stocka+ "-" + stockb + "-"+ fileBaseName(startTime, endTime)
        filePath = imageFolder +'/'  + filename
        # to be replaced by market data service
        dfa = web.DataReader(stocka, 'morningstar', startTime, endTime).reset_index()
        dfb = web.DataReader(stockb, 'morningstar', startTime, endTime).reset_index()

        tracea = go.Scatter(
                x=dfa.Date,
                y=dfa.Close,
                mode = 'lines',
                name = stocka)

        traceb = go.Scatter(x=dfb.Date,
                y=dfb.Close,
                mode = 'lines',
                name = stockb)

        layout = go.Layout(
            xaxis = dict(
                rangeslider = dict(
                    visible = False
                )
            )
        )
        data = [tracea, traceb]
        fig = go.Figure(data=data, layout=layout)
        
        plt.image.save_as(fig, filename=Path(filePath))

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

    def stockVWAP(self, stocka, startTime, endTime):
        filename = stocka+ "-VWAP-" + fileBaseName(startTime, endTime)
        filePath = imageFolder +'/'  + filename
        # to be replaced by market data service
        dfa = web.DataReader(stocka, 'morningstar', startTime, endTime).reset_index()

        dfa['vwap'] = (dfa.Volume*(dfa.High+dfa.Low)/2).cumsum() / dfa.Volume.cumsum()
        

        tracea = go.Scatter(
                x=dfa.Date,
                y=dfa.Close,
                mode = 'lines',
                name = stocka)

        traceb = go.Scatter(x=dfa.Date,
                y=dfa.vwap,
                mode = 'lines',
                name = 'vwap')

        layout = go.Layout(
            xaxis = dict(
                rangeslider = dict(
                    visible = False
                )
            )
        )
        data = [tracea, traceb]
        fig = go.Figure(data=data, layout=layout)
        
        plt.image.save_as(fig, filename=Path(filePath))

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

    def stockHistogram(self, stocka, startTime, endTime):
        filename = stocka+ "-histogram-" + fileBaseName(startTime, endTime)
        filePath = imageFolder +'/'  + filename
        # to be replaced by market data service
        dfa = web.DataReader(stocka, 'morningstar', startTime, endTime).reset_index()

        returns = (dfa.Close - dfa.Close.shift(1))/dfa.Close
        
        tracea = go.Histogram(x=returns,
                     histnorm='return percentage %')

        layout = go.Layout(
            xaxis = dict(
                rangeslider = dict(
                    visible = False
                )
            )
        )
        data = [tracea]
        fig = go.Figure(data=data, layout=layout)
        
        plt.image.save_as(fig, filename=Path(filePath))

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

    def capm(self, stocka, startTime, endTime):
        filename = stocka+ "-capm-" + fileBaseName(startTime, endTime)
        filePath = imageFolder +'/'  + filename
        # to be replaced by market data service
        df = web.DataReader(stocka, 'morningstar', startTime, endTime)
        fd = web.DataReader("spx", 'morningstar', startTime, endTime)
        
        return_index = fd.Close.pct_change()[1:]
        return_stock = df.Close.pct_change()[1:]

        y = return_stock.values
        x = return_index.values

        alpha, beta = linReg(x, y)

        x2 = np.linspace(x.min(), x.max(), 100)
        y_hat = x2*beta+alpha

        fig = mplot.figure()
        mplot.scatter(x,y,alpha=0.3)
        mplot.xlabel("index")
        mplot.ylabel(stocka)
        mplot.plot(x2,y_hat, "r", alpha=0.9)
        mplot.annotate('alpha: '+str(alpha)+", beta: "+str(beta), xy=(0.05, 0.95), xycoords='axes fraction')
        fig.savefig(Path(filePath))

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

