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


def Wday(month, day):
    """
    Function that yields the weekday given the month and the day for the year 2013,
        months 11 and 12
    Note that using this function to create the regression database acts as a
            substitution to normalizing the number of tweets to the individual weekday
                (as in: renormalizing a temporal serie)
    """
    out=["Mo","Tu","We","Th","Fr","Sa","Su"]
    if(month==11):
        return out[(4+day)%7]
    if(month==12):
        return out[(6+day)%7]


def scale(lst)
    """
    #asdkòashfàoabgaàsgfagd
    """

def df_reg(dfTweets, dfTemp):
    """
    Funzione che tratta il dataframe weather per produrre un dataframe
    con giorni e parametri utili per il ML
    """
    columnsDay=["Tweet1m", "Tweet2m", "Tavg1m", "Tavg2m", "Rainmax1m", "Rainmax2m",
                    "Rainavg1m", "Rainavg2m", "Electro1m", "Electro2m"]
    columnsNight = ["Tweet1n", "Tweet2n", "Tavg1n", "Tavg2n", "Rainmax1n", "Rainmax2n",
                  "Rainavg1n", "Rainavg2n", "Electro1n", "Electro2n"]
    columns=columnsDay+columnsNight+["Weekday","TargetDay", "TargetNight"]

    out=pd.DataFrame(columns=columns)

    ##Tweets:
    #NOTA: per ora il numero di tweets non sarà normalizzato ai giorni della settimana
    TwDay=dfTweets[dfTweets["hours"]>7.9]
    TwDay=TwDay[TwDay["hours"]<18.9]

    #Questo autosorta e raggruppa per day
    NtwDay = pd.DataFrame({'Counts': TwDay.groupby(
        ['month', 'day']).size()}).reset_index()
    out["TargetDay"]=NtwDay["Counts"]

    TwNight = dfTweets[dfTweets["hours"] > 18.9]

    NtwNight = pd.DataFrame({'Counts': TwNight.groupby(
        ['month', 'day']).size()}).reset_index()
    out["TargetNight"] = NtwDay["Counts"]

    #Per l'input dei twwets dei giorni prima, scorro il vettore inputs
    temp=list(NtwDay["Counts"])
    temp.insert(0, -1000)       #Insert front
    del temp[-1]                #Pop back
    out["Tweet1m"] = temp
    temp.insert(0, -1000)
    del temp[-1]
    out["Tweet2m"] = temp

    temp = list(NtwNight["Counts"])
    temp.insert(0, -1000)  # Insert front
    del temp[-1]  # Pop back
    out["Tweet1n"] = temp
    temp.insert(0, -1000)
    del temp[-1]
    out["Tweet2n"] = temp

    #Weekday
    temp=[]
    for i in [11, 12]:
        for j in range(0,19+i):
            temp.append(Wday(i,j))
    out["Weekday"]=temp

    #Average temperature
    #The average is computer over all the stations

    #All my homies hate weather database
    colTempDay=["date", "temperatures.0900", "temperatures.0915", "temperatures.0930", "temperatures.0945"]+\
               ["temperatures."+str(int(1000+100*np.floor(i/4)+(i%4)*15)) for i in range(0,36)]
    Tavg = pd.DataFrame(data=dfTemp, columns=colTempDay).groupby("date").mean()
    Tavg=list(Tavg.swapaxes(0,1).mean())

    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg1m"] = Tavg
    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg2m"]=Tavg

    colTempNight = ["temperatures." + str(int(1900 + 100 * np.floor(i / 4) + (i % 4) * 15)) for i in range(0, 20)]
    Tavg = pd.DataFrame(data=dfTemp, columns=colTempNight).groupby("date").mean()
    Tavg = list(Tavg.swapaxes(0, 1).mean())

    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg1m"] = Tavg
    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg2m"] = Tavg

    #Similarly, precipitation
    colPrecDay = ["date", "precipitations.0900", "precipitations.0915", "precipitations.0930", "precipitations.0945"] + \
                 ["precipitations." + str(int(1000 + 100 * np.floor(i / 4) + (i % 4) * 15)) for i in range(0, 36)]
    Tavg = pd.DataFrame(data=dfTemp, columns=colPrecDay).groupby("date").mean()
    Tavg = list(Tavg.swapaxes(0, 1).mean())

    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg1m"] = Tavg
    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg2m"] = Tavg

    colPrecNight = ["precipitations." + str(int(1900 + 100 * np.floor(i / 4) + (i % 4) * 15)) for i in range(0, 20)]
    Tavg = pd.DataFrame(data=dfTemp, columns=colPrecNight).groupby("date").mean()
    Tavg = list(Tavg.swapaxes(0, 1).mean())

    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg1m"] = Tavg
    del Tavg[-1]  # Pop back
    Tavg.insert(0, -1000)  # Insert front
    out["Tavg2m"] = Tavg


    out.drop(index=[0, 1], inplace=True)
    out.reset_index(inplace=True)
    out.drop(columns="index", inplace=True)
    print(out)
    return



