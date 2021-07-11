#####
import numpy as np
import pandas as pd

# custom lib
import sys
sys.path.append('./../src')

import make_dataset as m_d
import ML_functions as supp_ML

np.random.seed(86122330)


# PRIMA TASK: prevedere l'attività di twitter a livello provinciale
# Importo i dati dal database finale (vedi Import Dati)
data = pd.read_csv(m_d.data_path_out / 'MachineLearningDB.csv')

# Smisto target e features
target_mattina = data['TargetDay']
target_sera = data['TargetNight']
data.drop(columns=['TargetDay', 'TargetNight'], inplace=True)


num_feat=["Tweet1m", "Tweet2m", "Tweet1n", "Tweet2n", "Tavg1m", "Tavg2m", "Tavg1n", "Tavg2n"]
cat_feat=["Weekday"]


#MATTINA:
print("MATTINA:")
PL_Matt_Logistic=supp_ML.logistic_regressor_fittato(data, target_mattina, num_feat, cat_feat)
PL_Matt_RF=supp_ML.Random_Forest_Regressor_CV(data, target_mattina, num_feat, cat_feat)

print("\n\nSERA:")
PL_Sera_Logistic=supp_ML.logistic_regressor_fittato(data, target_sera, num_feat, cat_feat)
PL_Sera_RF=supp_ML.Random_Forest_Regressor_CV(data, target_sera, num_feat, cat_feat)


# SECONDA TASK: identificare la circoscrizione con più tweets associati
# creo il vettore delle y trovando qual è la circoscrizione più attiva
targetCirc = supp_ML.circoscrizione_attiva(m_d.data_path_out / "twitter_final.csv")
targetCirc = pd.Series(targetCirc)
targetCirc.drop([targetCirc.index[0], targetCirc.index[1]], inplace=True)
targetCirc.unique()  #Ho solo 2 valori rilevanti

PL_classPred=supp_ML.Random_Forest_Classifier_Circoscrizione(data, targetCirc, num_feat, cat_feat)

