#####
import numpy as np
import pandas as pd
import pickle
import random

# custom lib
import sys
sys.path.append('./../src')

import make_dataset as m_d
import ML_functions as supp_ML

seed=86122330
#NOTA: non so perchè ma usare GridSearchCV rovina il determinismo indotto dall'uso del seed di numpy
#Cercando online sembra non dovrebbe ma non sono troppo sicuro della questione
#Per ora cerco di aver quello che posso deterministico
#Poco male, considerando che visto il basso numero di dati eseguire multiple runs mostra quanto instabile l'outcome sia


# PRIMA TASK: prevedere l'attività di twitter a livello provinciale
# Importo i dati dal database finale (vedi Import Dati)
data = pd.read_csv(m_d.data_path_out / 'MachineLearningDB.csv')

# Smisto target e features
target_mattina = data['TargetDay']
target_sera = data['TargetNight']
data.drop(columns=['TargetDay', 'TargetNight'], inplace=True)


num_feat=["Tweet1m", "Tweet2m", "Tweet1n", "Tweet2n", "Tavg1m", "Tavg2m", "Tavg1n", "Tavg2n"]
cat_feat=["Weekday"]

np.random.seed(seed)
#MATTINA:
print("MATTINA:")
PL_Matt_Logistic=supp_ML.logistic_regressor_fittato(data, target_mattina, num_feat, cat_feat)
PL_Matt_RF=supp_ML.Random_Forest_Regressor_CV(data, target_mattina, num_feat, cat_feat)

np.random.seed(seed)
print("\n\nSERA:")
PL_Sera_Logistic=supp_ML.logistic_regressor_fittato(data, target_sera, num_feat, cat_feat)
PL_Sera_RF=supp_ML.Random_Forest_Regressor_CV(data, target_sera, num_feat, cat_feat)

np.random.seed(seed)
# SECONDA TASK: identificare la circoscrizione con più tweets associati
# creo il vettore delle y trovando qual è la circoscrizione più attiva
targetCirc = supp_ML.circoscrizione_attiva(m_d.data_path_out / "twitter_final.csv")
targetCirc = pd.Series(targetCirc)
targetCirc.drop([targetCirc.index[0], targetCirc.index[1]], inplace=True)

print("\nCLASSIFICATION:")
PL_classPred=supp_ML.Random_Forest_Classifier_Circoscrizione(data, targetCirc, num_feat, cat_feat)


filename1 = 'Mattina/Finalized_Logistic_morning.sav'
filename2 = 'Mattina/Finalized_RF_morning.sav'
pickle.dump(PL_Matt_Logistic, open(m_d.models_path / filename1, 'wb'))
pickle.dump(PL_Matt_RF, open(m_d.models_path / filename2, 'wb'))

filename1 = 'Sera/Finalized_Logistic_evening.sav'
filename2 = 'Sera/Finalized_RF_evening.sav'
pickle.dump(PL_Sera_Logistic, open(m_d.models_path / filename1, 'wb'))
pickle.dump(PL_Sera_RF, open(m_d.models_path / filename2, 'wb'))

filename1 = 'Circoscrizioni/Circoscrizioni.sav'
pickle.dump(PL_classPred, open(m_d.models_path / filename1, 'wb'))