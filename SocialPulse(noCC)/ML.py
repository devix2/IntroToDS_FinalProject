# Libreria per ML
"""
Prima task: prevedere l'attività di twitter a livello provinciale, iniziamo discretizzando
il tempo in bins di 30 minuti. Questo è dovuto al fatto che, grazie all'EDA, abbiamo osservato dei picchi di traffico 
specialmente nelle ore serali (da qui la necessità di avere una risoluzione temporale abbastanza fine) ma allo stesso 
tempo avendo 27k records in 62 giorni non volevamo avere dei binning con troppa poca popolazione. Da qui la nostra scelta
"""
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
import Supporto_ML as supp_ML

"""
Task 1: voglio cercare di predire il numero di tweets del giorno i-esimo a partire da alcuni parametri dei giorni i-1 e i-2.
I parametri scelti sono: numero di tweets, temperatura, precipitazioni e consumo di corrente elettrica
Si noti che i parametri sono dovutamente mediati sui ranges di interesse, che sono 8:00->18:59, 19:00->00:00(2.00)
I dati saranno quindi nella forma 
    X = ((Parametri giorno i-2),(parametri giorno i-1))
    y = #tweets giorno i"
"""

# Importo i dati dal database finale che abbiamo fatto queste sono le features di X
data = pd.read_csv('data/processed/MachineLearningDB.csv')

# Adesso creo il vettore target y
target_mattina = data['TargetDay']
target_sera = data['TargetNight']
data.drop(columns=['TargetDay', 'TargetNight'], inplace=True)

# Regressione a livello regionale
# Logistic Regressor
#supp_ML.logistic_regressor_fittato(data, target_mattina, 'mattina')
#supp_ML.logistic_regressor_fittato(data, target_sera, 'sera')

# Random Forest Regressor
#supp_ML.Random_Forest_Regressor_CV(data, target_mattina, 'mattina')
#supp_ML.Random_Forest_Regressor_CV(data, target_sera, 'sera')


"""
Adesso mi occupo di fare la parte di classificazione: voglio individuare quali siano le circoscrizioni di Trento che hanno
il più alto numero di interazioni sociali basandomi sui dati delle giornate precedenti. 
Il dataset sarà uguale a quello precedente con la differenza che la parte di conteggi delle X sarà divisa per circoscrizione
Dal momento che ci sono 12 circoscrizioni i parametri di input saranno 
[interazioni sociali giorno i-2 divisi per circoscrizione][interazioni sociali giorno i-1 divisi per circoscrizione] + altri parametri
Per quanto riguarda i target, considereremo la circoscrizione con il maggior numero di tweets.
Inizialmente provo a lavorare con un Classificatore random forest, dal momento che abbiamo pochi elementi
"""
# Random Forest Classifier
supp_ML.Random_Forest_Classifier_Circoscrizione(data)