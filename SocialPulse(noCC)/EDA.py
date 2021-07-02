from scipy import *
from numpy import *
import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
import numpy

#data_path = Path('./data/raw')   #Per Cookiecutter
data_path = Path('./data/raw')
# subdivide the time series
def date_divider(df):
    """
    This Fuction extracts the data from an undivided data format YYYY-MM-DDThh-mm-ss
    Where T stands for Time and has no further meaning
    """
    column_names = ["month", "day", "hours", "temperature", "rain"]
    out = pd.DataFrame(columns=column_names)
    N = len(df["created"])  # Numero tweets creati in un giorno
    for i in range(0, N):
        # Inizializzo ogni riga o crasha
        out.loc[i] = "NaN"
        # Tempo
        # Tw_final.loc[i]["year"]=int(tweets.loc[i]["created"][0:4])  #Chemmifrega dell'anno, tutti uguali
        out.loc[i]["month"] = int(df.loc[i]["created"][5:7])
        out.loc[i]["day"] = int(df.loc[i]["created"][8:10])
        out.loc[i]["hours"] = int(df.loc[i]["created"][11:13]) + 0.5 * (
            int(df.loc[i]["created"][14:16]) >= 30)
    return out
"""
#Temperatura, per ricavare questa usiamo la stazione più vicina al tweet (sfortunamente il Trentino non ne ha tante)
dmin=10000000000
for st in weather.groupby(station):
    d=tweets["geometry"].distance(st[geometry])
gdf['distance'] = gdf['centroid'].distance(queens_point)
Tw_final.loc[i]["temperature"]=int(tweets.loc[i]["created"][5:7])
"""


"""
    NB:
    Support class to divide the hours dataset
    """
subClas = {
    {"low": 0, "high": 0.5, "name": "Prima"},
    {"low": 0.5, "high": 1, "name": "Seconda"}
}

def Access_counter(df):
    """
    Please note that the data must be preprocessed by "date_divider" in order to work
    This function DOES NOT work with raw data
    This function assign a label to the minutes of the raw data in order to match them to the time resolution of the temperature aquisition.
    The result of this programme is a dictionair containing all the days!!
    """
    # I create a Support dictionary in order to get all the accesses subdivided by day
    dict = {}
    # Lunghezza is the number of elements
    lunghezza = 0
    mesi = df["month"].unique()
    for mese in mesi:
        temp = df[df["month"] == mese]
        lunghezza = lunghezza + len(temp['day'].unique())

    for j in range(0, lunghezza):
        bins = numpy.linspace(0, 0.5, 23.5)
        dict[j] = numpy.digitize(data, bins)
    return dict

