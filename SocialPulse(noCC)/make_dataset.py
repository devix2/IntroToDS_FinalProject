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




"""
def extract_temp(df)
    #Mi serve in primis creare un database delle stazioni della temperatura
    stazioni = weather['station'].unique()
    coltmpr=["nstation", "elevation", "temperature", "precipitations", "positio"]

    station_stats=pd.DataFrame(columns=coltmpr)

    colweather=weather.keys()

    for idx,stat in enumerate(stazioni):
        station_stats.loc[idx]="NaN"
        temp = weather[weather['station']==stat]

        #Costruiamo una mappa temporale per displayare la temperatura
        #Il tempo 0 è 1-11-2013 ore 0:00, e poi conto in minuti
        #L'ultimo elemento sarà un vettore con un integer in input e e una temperatura in output
        
        #temp['date'] =pd.to_datetime(temp["date"])
        #temp.sort('date')    #Sortiamo per sicurezza
        
        assert(len(temp["station"])==61), "Warning: length of the dataset does not match expected value"
        
            
        v=-1000*np.ones(1000000)
        #Chiedo venia per la python-unfriendlyness
        for j,st in enumerate(temp.Index()):
            for i,t in enumerate(colweather[7:7+4*24]):
                print(t)
                print(temp)
                v[(j*4*24+i)*15]=temp.loc[st][t]
        #Questo mappa effettivamente le colonne
        
        station_stats[idx]["postion"]=temp.loc[0]["geometry"]
        station_stats[idx]["station"]=stat
        station_stats[idx]["elevation"]=temp.loc[0]["elevation"]
        station_stats[idx]["temperature"]=v
        #Con temperature che sarà un dizionario che offre le temperature

station_stats
"""

