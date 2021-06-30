import pandas as pd
import numpy as np
import geopandas as gpd

from pathlib import Path

data_path = Path('./data/raw')

files = {'grid':'trentino-grid.geojson',
         'adm_reg':'administrative_regions_Trentino.json',
        'weather':'meteotrentino-weather-station-data.json',
        'precip':'precipitation-trentino.csv',
        'precip-avail':'precipitation-trentino-data-availability.csv',
        'SET-1':'SET-nov-2013.csv',
        'SET-2':'SET-dec-2013.csv',
        'SET-lines':'line.csv',
        'twitter':'social-pulse-trentino.geojson'}

def safe_import(filename, ftype):
    """
    Function that imports data from a file, turns it into a pandas dataframe,
    and prints the types of every variable to check for correctness of import
    """
    fl=data_path / files[filename]
    if(ftype=="geojson"):
        out=gpd.read_file(fl)

    print(out)

    return out




regions=safe_import("grid", "geojson")

