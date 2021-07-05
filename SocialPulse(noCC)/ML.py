# Libreria per ML
"""
Prima task: prevedere l'attività di twitter a livello provinciale, iniziamo discretizzando
il tempo in bins di 30 minuti. Questo è dovuto al fatto che, grazie all'EDA, abbiamo osservato dei picchi di traffico 
specialmente nelle ore serali (da qui la necessità di avere una risoluzione temporale abbastanza fine) ma allo stesso 
tempo avendo 27k records in 62 giorni non volevamo avere dei binning con troppa poca popolazione. Da qui la nostra scelta
"""
import pandas as pd
import numpy as np
import geopandas as gpd
import pandas as pd

# funzioni di sk-learn
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_validate
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.metrics import matthews_corrcoef, r2_score, accuracy_score, confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import train_test_split

# custom lib
# import make_dataset as m_d

# Importo i dati dal database finale che abbiamo fatto queste sono le features di X
data = pd.read_csv('data/processed/MachineLearningDB.csv')

# Adesso creo il vettore target y
twitter_data = pd.read_csv('data/processed/twitter_final.csv')
target = pd.DataFrame({'Counts': twitter_data.groupby(
        ['month', 'day']).size()}).reset_index()
target.drop([target.index[0], target.index[1]],inplace = True)
target = target['Counts'].to_numpy()

#Splitto train e test
X_train, X_test, y_train, y_test = train_test_split(data,target,test_size=0.4)

############### Parte di ML ###############
############### Random Forest Regressor ###############
pipe_logistic = Pipeline([
    ('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
    ('scaler', StandardScaler()),
    ('regressor', LogisticRegression())
])

pipe_logistic = pipe_logistic.fit(X_train, y_train)
y_logistic_pred = pipe_logistic.predict(X_test)
print(y_logistic_pred)
print("Lo score del nostro modello logistico risulta essere:", r2_score(y_test, y_logistic_pred))

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
pipe_RFR = Pipeline([
    ('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
    ('scaler', StandardScaler()),
    ('Regressor', RandomForestRegressor(bootstrap=False))
])
# Vale la pena fare un tentativo prima della CV che da un'accuracy 0
pipe_RFR.fit(X_train, y_train)
y_RF_pred = pipe_RFR.predict(X_test)
for i in range(len(y_RF_pred)):
    y_RF_pred[i] = int(y_RF_pred[i])
print(y_RF_pred - y_test)
print("Lo score della nostra Random Forest risulta essere:", r2_score(y_test, y_RF_pred))

# Provo con una grid search CV

CV_parameters = {'Regressor__n_estimators': [5, 10, 25, 50],
                 'Regressor__max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
                 'Regressor__max_features': ['auto', 'sqrt'],
                 'Regressor__min_samples_leaf': [1, 2, 4],
                 'Regressor__min_samples_split': [2, 5, 10],
                 }

# Parametri di Tuning del nostro RFR
grid_pipeline = GridSearchCV(estimator=pipe_RFR,
                             param_grid=CV_parameters,
                             verbose=10,
                             n_jobs=-1,)
grid_pipeline.fit(X_train,y_train)
y_RF_pred = grid_pipeline.predict(X_test)
print("Lo score della nostra Random Forest con CV risulta essere:", r2_score(y_test, y_RF_pred))

exit()

##################################################################
# Classificazione delle circoscrizioni di Trento
##################################################################
"""
Adesso mi occupo di fare la parte di classificazione: voglio individuare quali siano le circoscrizioni di Trento che hanno
il più alto numero di interazioni sociali basandomi sui dati delle giornate precedenti. 
Il dataset sarà uguale a quello precedente con la differenza che la parte di conteggi delle X sarà divisa per circoscrizione
Dal momento che ci sono 12 circoscrizioni i parametri di input saranno 
[interazioni sociali giorno i-2 divisi per circoscrizione][interazioni sociali giorno i-1 divisi per circoscrizione] + altri parametri

Per quanto riguarda i target, considereremo la circoscrizione con il maggior numero di tweets.


Inizialmente provo a lavorare con un Classificatore random forest, dal momento che abbiamo pochi elementi
"""

pipe_RFC = Pipeline([
    ('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
    ('scaler', StandardScaler()),
    ('Regressor', RandomForestClassifier())
])
# Vale la pena fare un tentativo prima della CV
pipe_RFC.fit(X_train, y_train)

# Provo con una grid search CV
# Questa griglia va ricontrollata
CV_parameters = {'bootstrap': [True, False],
                 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
                 'max_features': ['auto', 'sqrt'],
                 'min_samples_leaf': [1, 2, 4],
                 'min_samples_split': [2, 5, 10],
                 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
                 }
# Parametri di Tuning del nostro RFR
RFC_CV = GridSearchCV(estimator=pipe_RFC,
                      param_grid=CV_parameters,
                      n_jobs=-1,
                      cv=3,
                      verbose=100
                      )
best_RFC = RFC_CV.fit(X_train, y_train)
y_RFC_pred = best_RFC.predict(X_test)
print("Lo score della nostra Random Forest risulta essere:", accuracy_score(y_test, y_RFC_pred))
