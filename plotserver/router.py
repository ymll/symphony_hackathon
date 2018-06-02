import pandas_datareader as web
import plotly.graph_objs as go
import plotly.plotly as plt
from pathlib import Path
from flask import render_template
from pathlib import Path
from datetime import datetime

plt.sign_in('jerrydeng', '19KIrNZ6zRN48QjsMdGg') # Replace the username, and API key with your credentials.

imageFolder = "static"
stockChartBaseName = "-simple-plot.png"
stockTemplate = "stock.html"

class Router:
    def getStock(self, stockname, startTime, endTime):
        filename = stockname + startTime.isoformat() + '-' + endTime.isoformat() +stockChartBaseName
        filePath = imageFolder +'/'  + filename

        if True or not Path(filePath).exists():

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
            
            plt.image.save_as(fig, filename=filePath)

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

    def compareStock(self, stocka, stockb, startTime, endTime):
        filename = stocka+ "-" + stockb + "-"+ startTime.isoformat() + '-' + endTime.isoformat() \
            + datetime.now().isoformat() +stockChartBaseName
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
        
        plt.image.save_as(fig, filename=filePath)

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)

    def stockVWAP(self, stocka, startTime, endTime):
        filename = stocka+ "-VWAP"  + "-"+ startTime.isoformat() + '-' + endTime.isoformat() \
            + datetime.now().isoformat() +stockChartBaseName
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
        
        plt.image.save_as(fig, filename=filePath)

        return render_template(stockTemplate,
                           imageFolder=imageFolder,
                           fileName=filename)


