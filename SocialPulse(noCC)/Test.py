
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import Point, Polygon


from functions import *
import make_dataset as m_d

weather_json = json.load( open(m_d.data_path / m_d.files['weather'][0]) )
weather = gpd.GeoDataFrame(weather_json['features'])


#Elimino le colonne del vento (dati molto incompleti)
weather.drop(weather.columns[list(range(202,298))], axis=1, inplace=True)
weather.drop(columns=['minWind', "maxWind"], inplace=True)

#Svolgiamo infine i punti geometrici
weather['geometry'] = weather['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
weather.drop(columns=['geomPoint.geom'],inplace=True)

pd.set_option('display.max_columns', None)
weather.head(5)




Tw_final=pd.read_csv("data/processed/twitter_final.csv")


a=m_d.df_reg(Tw_final,weather)
