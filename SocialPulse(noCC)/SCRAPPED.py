
















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