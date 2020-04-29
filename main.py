from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import register_matplotlib_converters
from sklearn.metrics import mean_squared_error
register_matplotlib_converters()

app = Flask(__name__)
@app.route('/')
def index():
    df2 = pd.read_csv("static/literacy.csv")
    df_total = pd.read_csv("static/file1.csv")
    df_temp = pd.read_csv("static/temparature.csv")
    df_annualChange = pd.read_csv("static/file2.csv")
    df_output = pd.read_csv("static/output.csv")
    df_industry = pd.read_csv("static/industry.csv")
    df_vehicle = pd.read_csv("static/vehicle.csv")
    data_vehicle = [
        go.Scatter(y = df_vehicle.totalvehicles, x=df_vehicle.year,name= "Number of Vehicles" , mode = "lines+markers"),
    ]
    data_large_building = [
        go.Scatter( y= df_industry.ItCount , x = df_industry.Year, name = "Count of Large Buildings", mode = "markers"),
    ]
    data_industry_gdp = [
        go.Scatter(y = df_industry.Industry, x=df_industry.Year,name= "Various" , mode = "lines"),
        go.Scatter(y = df_industry.IT, x=df_industry.Year,name= "IT" , mode = "lines"),
        go.Scatter(y = df_industry.Construction, x=df_industry.Year,name= "Construction" , mode = "lines"),
        go.Scatter(y = df_industry.Manufacting, x=df_industry.Year,name= "Manufacturing" , mode = "lines")
    ]
    data_industry_diff = [
        go.Scatter(y = df_industry.industrychange, x=df_industry.Year,name= "Various" , mode = "lines"),
        go.Scatter(y = df_industry.itchange, x=df_industry.Year,name= "IT" , mode = "lines"),
        go.Scatter(y = df_industry.constchange, x=df_industry.Year,name= "Construction" , mode = "lines"),
        go.Scatter(y = df_industry.manuchange, x=df_industry.Year,name= "Manufacturing" , mode = "lines")
    ]
    data_output = [
        go.Scatter(x = df_output.Year , y = df_output.Input , name="Seen"),
        go.Scatter(x = df_output.Year , y = df_output.Output , name = "Predicted"),
        go.Scatter(x = df_output.Year , y = df_output.Lower ,name = "Lower", line=dict(color='grey', width=2, dash='dot') ),
        go.Scatter(x = df_output.Year , y = df_output.Upper ,name = "Upper",fill='tonexty', line=dict(color='grey', width=2, dash='dot') )
    ]
    data_population = [
        go.Bar(x=df2.date, y=df2["Literate"], name='Literate'),
        go.Bar(x=df2.date, y=df2["Illiterate"], name='Illiterate'),
        go.Scatter(x=df2.date, y=df_total["Population"], name='Population',mode='lines'),
    ]
    data_annualChange = [
        go.Scatter(x=df_annualChange.date , y = df_annualChange["AnnualChange"],name = "AnnualChange")
    ]
    data_literacy = [
        go.Bar(
            x = [1951,1961,1971,1981,1991,2001,2011],
            y = [27.91,35.08,45.77,57.24,64.87,76.88,82.3]
        )
    ]
    data_temp = [
        go.Scatter(x=df_temp.YEAR, y=df_temp.ANNUAL, name='Annual',mode='lines+markers',line=dict(color='royalblue', width=4)),
        go.Scatter(x=df_temp.YEAR, y=df_temp["JAN-FEB"], name = 'Jan-Feb',mode='markers'),
        go.Scatter(x=df_temp.YEAR, y=df_temp["MAR-MAY"], name='Mar-May',mode='markers'),
        go.Scatter(x=df_temp.YEAR, y=df_temp["JUN-SEP"], name='Jun-Sep',mode='markers'),
        go.Scatter(x=df_temp.YEAR, y=df_temp["OCT-DEC"], name='Oct-Dec',mode='markers')]  
    data_total = [
        go.Line(
            x=df_total.date,
            y=df2.TempTotal
        )
    ]
    industies = ["IT","Manufacturing","Construction","Trade","Market","Transport","Commodities","Utils"]
    industies_val = [28.3,18.4,6.3,14.7,11.3,9.8,9.6,6.4]
    data_pie_industry = [
        go.Pie(labels =industies ,values =industies_val  ,pull=[0.2, 0.2, 0.2, 0,0,0,0,0] )
        ]
    json_large_building = json.dumps(data_large_building,cls=plotly.utils.PlotlyJSONEncoder)
    json_vehicle = json.dumps(data_vehicle,cls=plotly.utils.PlotlyJSONEncoder)
    json_ind_gdp = json.dumps(data_industry_gdp,cls=plotly.utils.PlotlyJSONEncoder)
    json_ind_diff = json.dumps(data_industry_diff,cls=plotly.utils.PlotlyJSONEncoder)
    json_pie = json.dumps(data_pie_industry,cls=plotly.utils.PlotlyJSONEncoder)
    json_total = json.dumps(data_total, cls=plotly.utils.PlotlyJSONEncoder)
    json_output = json.dumps(data_output, cls=plotly.utils.PlotlyJSONEncoder)
    json_population = json.dumps(data_population, cls=plotly.utils.PlotlyJSONEncoder)
    json_temperature = json.dumps(data_temp, cls=plotly.utils.PlotlyJSONEncoder)
    json_literacy = json.dumps(data_literacy, cls=plotly.utils.PlotlyJSONEncoder)
    json_annualChange = json.dumps(data_annualChange, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html",json_large_building=json_large_building,json_vehicle = json_vehicle , json_ind_diff=json_ind_diff,json_ind_gdp=json_ind_gdp   , json_annualChange=json_annualChange,json_temperature=json_temperature,   json_total = json_output,json_population = json_population , json_literacy = json_literacy,json_pie=json_pie)
if __name__ == '__main__':
    app.run(debug=True)