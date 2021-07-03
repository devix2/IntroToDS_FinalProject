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
        'regions':['Com01012013/Com01012013_WGS84.shp',"shape"],
        'circoscrizioni':['CircoscrizioniTN/circoscrizioni.shp',"shape"]}

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
    if(filetype=="json"):
        out=pd.read_json(fl, orient="values")
    if(filetype=="shape"):
        out=gpd.read_file(fl)
    print(out.keys())
    

    return out




"""
######## PER ORA NON USIAMO QUESTA, DA' SERI PROBLEMI, è QUASI COMPLETA MA è MOLTO POCO ELEGANTE
def extract_temp(df)
    #Mi serve in primis creare un database delle stazioni della temperatura
    stazioni = weather['station'].unique()
    coltmpr=["station", "elevation", "temperature", "precipitations", "geometry"]

    station_stats=gpd.GeoDataFrame(columns=coltmpr)

    colweather=weather.keys()

    for idx,stat in enumerate(stazioni):
        station_stats.loc[idx]="NaN"
        
        temp = pd.DataFrame(weather[weather['station']==stat])
        
        
        #Costruiamo una mappa temporale per displayare la temperatura
        #Il tempo 0 è 1-11-2013 ore 0:00, e poi conto in minuti
        #L'ultimo elemento sarà un vettore con un integer in input e e una temperatura in output

        temp['date'] =pd.to_datetime(temp["date"])
        #temp.sort('date')    #Sortiamo per sicurezza

        assert(len(temp["station"])==61), "Warning: length of the dataset does not match expected value"

        v=-1000*np.ones(10000)
        #Chiedo venia per la python-unfriendlyness
        for j,st in enumerate(temp.index):
            for i,t in enumerate(colweather[7:7+4*24]):
                v[(j*4*24+i)*15]=temp.loc[st][t]
        #Questo mappa effettivamente le colonne
        
        
        station_stats.loc[idx]["geometry"]=temp.loc[temp.index[0],:]["geometry"]
        station_stats.loc[idx]["station"]=stat
        station_stats.loc[idx]["elevation"]=temp.loc[temp.index[0],:]["elevation"]
        station_stats.loc[idx]["temperature"]=v
        #Con temperature che sarà un dizionario che offre le temperature

station_stats

"""

def orderstation(weatherdf):
    """
    Funzione che ordina il dataframe del weather per estrarre caratteristiche uniche delle stazioni, quali nome, posizione, elevazione
    Comodo quando devo trovare la stazione più vicina ad un punto
    """

    stazioni = weatherdf['station'].unique()
    coltmpr=["station", "elevation", "geometry"]

    station_stats=gpd.GeoDataFrame(columns=coltmpr)

    for idx,stat in enumerate(stazioni):
        temp = pd.DataFrame(weatherdf[weatherdf['station']==stat])
        station_stats.loc[idx]="NaN"
        
        station_stats.loc[idx]["geometry"]=temp.loc[temp.index[0],:]["geometry"]
        station_stats.loc[idx]["station"]=stat
        station_stats.loc[idx]["elevation"]=temp.loc[temp.index[0],:]["elevation"]
    return station_stats


def find_temperature(weatherdf, month, day, hour, stationName):
    """
    Funzione che trova il valore di temperatura dentro weatherdf corretto per una certa data fornita
    """
    cellname=str(int(np.floor(hour)*100+(hour%1)*60))
    while(len(cellname)<4):
        cellname="0"+cellname
    cellname="temperatures."+cellname


    df=weatherdf[weatherdf['station']==stationName]
    if(day<10):
        df=df[df['date']=="2013-"+str(month)+"-0"+str(day)]
    else:
        df=df[df['date']=="2013-"+str(month)+"-"+str(day)]

    #Se manca il dato lo prendo mezz'ora prima o dopo che non varia troppo
    """
    try:
        return float(str(df[cellname]))
    except ValueError:
        if(hour>=0.5):
            return find_temperature(weatherdf, month, day, hour-0.5, stationName)
        else:
            return find_temperature(weatherdf, month, day, hour+0.5, stationName)
    """
    """
    if(len(str(df[cellname]))<1 and hour>=0.5):
        return find_temperature(weatherdf, month, day, hour-0.5, stationName)
    elif(len(str(df[cellname]))<1):
        return find_temperature(weatherdf, month, day, hour+0.5, stationName)
    """
    if(df[cellname].isnull().all()):
        if(hour>=0.5):
            return find_temperature(weatherdf, month, day, hour-0.5, stationName)
        else:
            return find_temperature(weatherdf, month, day-1, 23.5, stationName)
    return float(df[cellname])
    

def find_precipitation(weatherdf, month, day, hour, stationName):
    """
    Funzione che trova il valore di precipitazione dentro weatherdf corretto per una certa data fornita
    A far bene la mergio alla funzione sopra che sono identiche
    """
    cellname=str(int(np.floor(hour)*100+(hour%1)*60))
    while(len(cellname)<4):
        cellname="0"+cellname
    cellname="precipitations."+cellname


    df=weatherdf[weatherdf['station']==stationName]
    if(day<10):
        df=df[df['date']=="2013-"+str(month)+"-0"+str(day)]
    else:
        df=df[df['date']=="2013-"+str(month)+"-"+str(day)]
    
    if(df[cellname].isnull().all()):
        if(hour>=0.5):
            return find_precipitation(weatherdf, month, day, hour-0.5, stationName)
        else:
            return find_precipitation(weatherdf, month, day-1, 23.5, stationName)
    return float(df[cellname])



def mediate_parameters(df)
    """
    Funzione che tratta il dataframe weather per produrre un dataframe
    con giorni e parametri utili per il ML
    """
    columns=["month", "day", "T_avg_mor", "T_avg_aft", "Rain_max", "Rain_avg", "T_avg"]
    out=pd.DataFrame()


    for i in df.groupby(columns="date")


