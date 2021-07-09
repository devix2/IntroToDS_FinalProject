#####
import numpy as np
import geopandas as gpd
import pandas as pd


####### VEDERE COSA VA EFFETTIVAMENTE IMPORTATO
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
import ML_functions as supp_ML

np.random.seed(86122330)

"""
Task 1: voglio cercare di predire il numero di tweets del giorno i-esimo a partire da alcuni parametri dei giorni i-1 e i-2.
I parametri scelti sono: numero di tweets, temperatura, precipitazioni e consumo di corrente elettrica
Si noti che i parametri sono dovutamente mediati sui ranges di interesse, che sono 8:00->18:59, 19:00->00:00(2.00)
I dati saranno quindi nella forma 
    X = ((Parametri giorno i-2),(parametri giorno i-1))
    y = #tweets giorno i"
"""

# Importo i dati dal database finale che abbiamo fatto queste sono le features di X
# tratto i dati forniti come categorici mediante un one hot encoder, non
data = pd.read_csv('data/processed/MachineLearningDB.csv')
enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
data['Weekday'] = enc.fit_transform(data['Weekday'].values[:,None])
# Adesso creo il vettore target y
target_mattina = data['TargetDay']
target_sera = data['TargetNight']
data.drop(columns=['TargetDay', 'TargetNight'], inplace=True)



print("Regressione a numero di tweets, livello regionale")
print("MATTINA:")
supp_ML.logistic_regressor_fittato(data, target_mattina)
supp_ML.Random_Forest_Regressor_CV(data, target_mattina)

print("\n\nSERA:")
supp_ML.logistic_regressor_fittato(data, target_sera)
supp_ML.Random_Forest_Regressor_CV(data, target_sera)
# Random Forest Regressor



"""
Task 2: voglio individuare quali siano le circoscrizioni di Trento che hanno
il più alto numero di interazioni sociali basandomi sui dati delle giornate precedenti. 
Il dataset sarà uguale a quello precedente con la differenza che la parte di conteggi delle X sarà divisa per circoscrizione
Dal momento che ci sono 12 circoscrizioni i parametri di input saranno 
[interazioni sociali giorno i-2 divisi per circoscrizione][interazioni sociali giorno i-1 divisi per circoscrizione] + altri parametri
Per quanto riguarda i target, considereremo la circoscrizione con il maggior numero di tweets.
Inizialmente provo a lavorare con un Classificatore random forest, dal momento che abbiamo pochi elementi
"""
# Random Forest Classifier
##supp_ML.Random_Forest_Classifier_Circoscrizione(data)

#QUESTA SI FIXI PRIMA CHE CI OPERO PER ABBELLIRLA


#SERVE INOLTRE AGGIUNGERE LA ML ANALYSIS, DIREI CHE FAI TU
#A FAR BENE SI SALVANO I MODELLI, VABBè CHE VISTO IL TRAINING DI 1 MINUTI ANCHE CHISSENE