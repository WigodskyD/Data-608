import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import csv
import urllib3
import requests
import math
from flask import Flask, request, render_template,jsonify
#import jsonify

df = pd.read_csv('https://raw.githubusercontent.com/WigodskyD/data-sets/master/NYC_Map_Data.csv')
df.columns.values[0] = 'index'
print(df.head(n=10))

#----------------------------------
#choose genre


def filter_genre(genre, datafr=df):
    genre_filter = genre[0:3]
    filterer = datafr['movies_genre'].str.contains(genre_filter)
    df_filtered = datafr[filterer]
    return df_filtered


print(filter_genre('Mystery', df))
#----------------------------------
#choose year


def filter_year(year, datafr=df):
    year_set = int(math.floor(year/10)*10)
    year_set_bool = datafr['movies_year'] - year_set < 10
    df_filtered_yr = datafr[year_set_bool]
    year_set_bool = df_filtered_yr['movies_year'] - year_set > -1
    df_filtered_yr = df_filtered_yr[year_set_bool]
    return df_filtered_yr


print(filter_year(1979, df)['movies_year'])
#----------------------------------

latitude = list(df['movies_lat'])
longitude = list(df['movies_long'])
movie_names = list(df['movies_names'])
print(df.columns)
print(latitude)
print(type(latitude))


trace=dict(
    locationmode="USA-states",
    type='scattergeo',
    lon=[-73.9712, -73.9442], lat=[40.7831, 40.6782],
    mode='markers')

#py.plot([trace], filename='NYC_map')

mapbox_access_token = 'pk.eyJ1IjoiZGFud2lnIiwiYSI6ImNqcDdvamp0dTB2cmYza3FzeDN3ZW05OGEifQ.OzM_HzpiAcFeJLb21l2xPA'

data = [
    go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode='markers',
        marker=dict(
            size=14
        ),
        text=movie_names,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=40.7638,
            lon=-73.9795
        ),
        pitch=0,
        zoom=10
    ),
)

fig = dict(data=data, layout=layout)
config= {'displayModeBar': False, 'scrollZoom': True}
#py.plot(fig, filename='NYC_map', config=config)



dfb = filter_genre('Fantasy')
dfb = filter_year(1989, dfb)
print(dfb['movies_year'])
print(dfb['movies_genre'])
print(dfb['movies_names'])
print(dfb.to_json())
#------------------------------------------------------------------
app = Flask(__name__)
@app.route('/')
def main_show():
    return pageframeA()


@app.route('/clicki')
def zoom_to_i():
    lat_input = 40.697
    lon_input = -73.843
    zoom_level = 11
    layout_input = layout_setter(lat_input, lon_input, zoom_level)
    fig = dict(data=data, layout=layout_input)
    plot(fig, filename='NYC_map', config=config)
    return pageframeB()

@app.route('/clickd')
def zoom_to_d():
    lat_input = 40.7336
    lon_input = -74.0028
    zoom_level = 13
    layout_input = layout_setter(lat_input, lon_input, zoom_level)
    fig = dict(data=data, layout=layout_input)
    plot(fig, filename='NYC_map', config=config)
    return pageframeB()

@app.route('/interactive')
def interactive():
    return render_template("buttons.html")


@app.route('/_background_process', methods=['GET', 'POST'])
def get_data():
    #input_to_python=request.args.get('input_to_pass')

    return dfb.to_json()