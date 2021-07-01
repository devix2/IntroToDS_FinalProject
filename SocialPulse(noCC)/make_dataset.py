import pandas as pd
import numpy as np
import geopandas as gpd

from pathlib import Path

#data_path = Path('./data/raw')   #Per Cookiecutter
data_path = Path('./data/raw')



files = {'grid':['trentino-grid.geojson',"geojson"],
        'adm_reg':['administrative_regions_Trentino.json',"json"],
        'weather':['meteotrentino-weather-station-data.json',"json"],
        'precip':['precipitation-trentino.csv',"csv"],
        'precip-avail':['precipitation-trentino-data-availability.csv',"csv"],
        'SET-1':['SET-nov-2013.csv',"csv"],
        'SET-2':['SET-dec-2013.csv',"csv"],
        'SET-lines':['line.csv',"csv"],
        'twitter':['social-pulse-trentino.geojson',"json"],
        'regions':['Com01012013/Com01012013_WGS84.shp',"shape"]}

def safe_import(inp):
    """
    Function that imports data from a file, turns it into a pandas dataframe,
    and prints the types of every variable to check for correctness of import
    """
    filename=files[inp][0]
    filetype=files[inp][1]

    fl=data_path / filename
    if(filetype=="geojson"):
        out=gpd.read_file(fl)
    if(filetype=="csv"):
        out=pd.read_csv(fl)
        ##### DA FIXARE
    if(filetype=="json"):
        out=pd.read_json(fl, orient="values")
    if(filetype=="shape"):
        out=gpd.read_file(fl)
    print(out.keys())
    

    return out





