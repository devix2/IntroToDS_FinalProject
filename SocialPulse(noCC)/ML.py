# Libreria per ML
"""
Iniziamo con la prima task, ovvero prevedere l'attività di twitter a livello provinciale, iniziamo discretizzando
il tempo in bins di 30 minuti. Questo è dovuto al fatto che, grazie all'EDA, abbiamo osservato dei picchi di traffico 
specialmente nelle ore serali (da qui la necessità di avere una risoluzione temporale abbastanza fine) ma allo stesso 
tempo avendo 27k records in 62 giorni non volevamo avere dei binning con troppa poca popolazione. Da qui la nostra scelta
"""
import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
import numpy
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from functions import *
import seaborn as sns
from numpy import linspace
import json
from shapely.geometry import Point

# funzioni di sk-learn
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegressionCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_validate
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.metrics import matthews_corrcoef, accuracy_score, confusion_matrix, plot_confusion_matrix
from pandas_profiling import ProfileReport
from sklearn.model_selection import train_test_split

#custom lib
#import make_dataset as m_d

# Importo i dati di Weather, TO BE REMOVED ###############

weather_json = json.load( open(m_d.data_path / m_d.files['weather'][0]) )
weather = gpd.GeoDataFrame(weather_json['features'])
#Elimino le colonne del vento (dati molto incompleti)
weather.drop(weather.columns[list(range(202,298))], axis=1, inplace=True)
weather.drop(columns=['minWind', \"maxWind\"], inplace=True)
#Svolgiamo infine i punti geometrici\n
weather['geometry'] = weather['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
weather.drop(columns=['geomPoint.geom'],inplace=True)
pd.set_option('display.max_columns', None)
weather.head(5)


############### Parte di ML ###############
############### Random Forest Regressor ###############
# Sono dubbioso sull'effettiva efficacio di questa pipeline però un tentativo và sicuramente fatto!
"""
Task 1: voglio cercare di predire il numero di tweets del giorno i-esimo a partire da alcuni parametri dei giorni i-1 e i-2.
I parametri scelti sono: numero di tweets, temperatura, precipitazioni e consumo di corrente elettrica
Si noti che i parametri sono dovutamente mediati sui ranges di interesse, che sono 8:00->18:59, 19:00->00:00(2.00)
I dati saranno quindi nella forma 
    X = ((Parametri giorno i-2),(parametri giorno i-1))
    y = #tweets giorno i"
"""
pipe_RF = Pipeline([
            ('encoder', OneHotEncoder(sparse = False, handle_unknown = 'ignore' )),
            ('scaler', StandardScaler()),
            ('Regressor', RandomForestRegressor())   #IMPORTATE: dare i parametri alla RFR
    ])
# ale la pena fare un tentativo prima della CV
pipeRF.fit(X_train, y_train)


# Provo con una grid search CV

CV_parameters = {'bootstrap': [True, False],
 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
                }
# Parametri di Tuning del nostro RFR
RFR_CV = GridSearchCV(estimator = pipe_RF,
                      param_grid = CV_parameters,
                      n_jobs = -1,
                      cv = 3,
                      verbose=100
                      )
best_RF = RFR_CV.fit(X_train, y_train)
y_RF_pred = best_RF.predict(X_test)
print(\"Lo score della nostra Random Forest risulta essere: \", accuracy_score(y_test, y_pred_test))"