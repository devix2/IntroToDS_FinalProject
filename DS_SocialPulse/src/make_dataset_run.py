import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import Point, Polygon

#Per usare multi cartelle (cookiecutter)
import sys
sys.path.append('./../src')

import make_dataset as m_d

"""
Python script that imports all the data necessary and
    creates the refined databases within data/processed
Note: it is probably wiser to use import.ipynb to run the scripts, as it drastically
    increases understandability and allows for some nice plots
"""

################# IMPORT #####################
## Grid
grid=m_d.safe_import("grid")



### Social pulse ###
#Questo fallisce ad importare, come mostrato a lezione 24
tweets_json = json.load( open(m_d.data_path_in / m_d.files['twitter'][0]) )
tweets = gpd.GeoDataFrame(tweets_json['features'])


#Creiamo il punto smontando la casella point
tweets['geometry'] = tweets['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
tweets.drop(columns=['geomPoint.geom'],inplace=True)

#Droppo roba inutile
tweets.drop(columns=['municipality.acheneID'],inplace=True)
tweets.drop(columns=['entities'],inplace=True)



### Weather ###
#Analogo a sopra
weather_json = json.load( open(m_d.data_path_in / m_d.files['weather'][0]) )
weather = gpd.GeoDataFrame(weather_json['features'])

#Elimino le colonne del vento (dati molto incompleti)
weather.drop(weather.columns[list(range(202,298))], axis=1, inplace=True)
weather.drop(columns=['minWind', "maxWind"], inplace=True)

#Svolgiamo infine i punti geometrici
weather['geometry'] = weather['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
weather.drop(columns=['geomPoint.geom'],inplace=True)

#Lo salvo che mi serve in sezione ML
weather.to_csv(m_d.data_path_out / 'weather_final.csv',index=False)

#Also creo dataframe stazioni
stations=m_d.orderstation(weather)



### Precipitazioni ###
#Non metto qua, vedi notebook



### Electro ###
#Problema: il primo dato vien preso come dizionario
#Converto colonne
electro = m_d.safe_import('SET-1')
electro=electro.rename(columns={'DG1000420': 'LINESET', "2013-11-01 00:00": 'Timestamp', "37.439999" : 'Value Amp'})
#Riaggiungo il primo dato
electro=m_d.appforth(electro,['DG1000420','2013-11-01 00:00',37.439999])

temp = m_d.safe_import('SET-2')
temp=temp.rename(columns={'DG1000420': 'LINESET', "2013-12-01 00:00": 'Timestamp', "36.719997" : 'Value Amp'})
#Riaggiungo il primo dato
temp=m_d.appforth(temp,['DG1000420','2013-12-01 00:00',36.719997])

electro=electro.append(temp, ignore_index=True)

#Unisco a dataframe che descrive posizioni sulla griglia
#Ne faccio un secondo che per alcune operazione è più comodo operare con l'altro
lines = m_d.safe_import('SET-lines')
electroLines = electro.merge(right=lines, how='outer')

#Ci sono incompatibilità tra i record salvati quindi li droppo cattivo
electroLines = electroLines.dropna()

#Serve svolgere il timestamp
temp=list(electro["Timestamp"])
electro["month"]=[int(st[5:7]) for st in temp]
electro["day"]=[int(st[8:10]) for st in temp]
#electro["hours"]=[int(st[11:13])+int(st[14:16])/60 for st in temp]
electro["hours"]=[np.around(int(st[11:13])+int(st[14:16])/60, 2) for st in temp]
    #Round per safer groupby, albeit slower (should not matter, just print uniques)
    #Utile che fa anche un file più leggero
#print(electro.hours.unique())
    
electro.drop(columns=["Timestamp"], inplace=True)
electro.to_csv(m_d.data_path_out / 'electro_final.csv',index=False)
    #Lo salvo che mi serve altrove, e questo è lenta da eseguire



### Circoscrizioni ###
#Friendship ended with database del prof, database della provincia is now my best friend
circ=m_d.safe_import('circoscrizioni')

circ.plot("area")
circ=circ.sort_values("numero_cir").reset_index()
circ.drop(columns=["index", "numero_cir"], inplace=True)
#Sistemo per riallacciare
circ.drop(columns=["fumetto", "area", "perimetro"],inplace=True)
circ.rename(columns={"nome" : "circoscrizione"}, inplace=True)




################# DATABASE MERGING #####################
### Database tweets ###
tweets=tweets.set_crs("EPSG:4326")
circ=circ.to_crs("EPSG:4326")
tweets = gpd.sjoin(tweets, grid, how="inner", op='intersects')
tweets.drop(columns="index_right", inplace=True)
tweets = gpd.sjoin(tweets, circ, how="left", op='intersects') 
    #Questi li attacco anche se potrei usare dirretto la grid, così è più comodo
tweets.drop(columns="index_right", inplace=True)

from shapely.ops import nearest_points


Tw_final=pd.DataFrame()

N=len(tweets["created"])  #Numero tweets
temp=tweets["created"]
#TEMPO va smontato
Tw_final["month"]=[int(st[5:7]) for st in temp]
Tw_final["day"]=[int(st[8:10]) for st in temp]
Tw_final["hours"]=[int(st[11:13])+0.5*(int(st[14:16])>=30) for st in temp]

# TEMPERATURA E PRECIPITAZIONI
# per ricavare queste usiamo la stazione più vicina al tweet
# (sfortunamente il Trentino non ne ha tante, fortunatamente sono distribuite bene)
    
T=[]
R=[]

#Voglio farlo pythonico e rapido, quindi si userà nearest point
    #(ironicamente builtin sembra più lenta, si può ottimizzare ulteriormente)
#Vedi notebook note informative per una very very basic overview
nearest=[ stations[stations["geometry"]==nearest_points(gm,
            gpd.GeoSeries(stations["geometry"]).unary_union)[1]]["station"].values[0] for gm in tweets["geometry"]]
    #lista con nome della stazione più vicina

#Questo è ancora migliorabile come forma
for i in range(0,N):
    T.append(m_d.find_Weather(weather, Tw_final.loc[i]["month"],
                                Tw_final.loc[i]["day"], Tw_final.loc[i]["hours"], nearest[i], varType=0))
    R.append(m_d.find_Weather(weather, Tw_final.loc[i]["month"],
                                Tw_final.loc[i]["day"], Tw_final.loc[i]["hours"], nearest[i], varType=1))
Tw_final["temperature"]=T
Tw_final["rain"]=R

#Il resto lo importo direttamente
Tw_final["municipal"]=tweets["municipality.name"]
Tw_final["cellId"]=tweets["cellId"]
Tw_final["language"]=tweets["language"]
Tw_final["circoscrizione"]=tweets["circoscrizione"]

#Salviamo infine il database
Tw_final.to_csv(m_d.data_path_out / 'twitter_final.csv', index=False)



### Regression Database (days) ###
regressdB=m_d.df_reg()
regressdB.to_csv(m_d.data_path_out / 'MachineLearningDB.csv', index=False)

regressdB.head(10)







