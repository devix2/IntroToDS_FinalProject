# Libreria per ML
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
from sklearn.metrics import plot_roc_curve, plot_precision_recall_curve, plot_confusion_matrix
from sklearn.model_selection import train_test_split

# custom lib
import make_dataset as m_d

################# REGRESSIONE A NUMERO DI TWEETS
#Logistic
def logistic_regressor_fittato(X,y):
    """
    Funzione che crea, fitta, testa e ritorna una pipeline con il logistic regressor,
    con alcune caratterstiche autoevidenti da codice
    Printa il risultato dell'r2 score
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    pipe_logistic = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        ('scaler', StandardScaler()),
        ('regressor', LogisticRegression())
    ])

    pipe_logistic = pipe_logistic.fit(X_train, y_train)
    y_logistic_pred = pipe_logistic.predict(X_test)
    print("Logistic regression r2_score =", r2_score(y_test, y_logistic_pred))
    return pipe_logistic




#Random forest
def Random_Forest_Regressor_CV(X,y):
    """
    Funzione che crea, fitta, testa e ritorna una pipeline con il RF regressor,
    con alcune caratterstiche autoevidenti da codice
    Printa il risultato dell'r2 score
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    pipe_RFR = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        ('scaler', StandardScaler()),
        ('Regressor', RandomForestRegressor(bootstrap=False))
    ])
    # Vale la pena fare un tentativo prima della CV che da un'accuracy 0
    pipe_RFR.fit(X_train, y_train)
    y_RF_pred = pipe_RFR.predict(X_test)
    for i in range(len(y_RF_pred)):
        y_RF_pred[i] = int(y_RF_pred[i])
    print("Random forest r2_score = ", r2_score(y_test, y_RF_pred))

    # Provo con una grid search CV
    CV_parameters = {'Regressor__n_estimators': [5, 10, 25, 50],
                     'Regressor__max_depth': [10, 20, 50, 70, 100, None],
                     'Regressor__max_features': ['auto', 'sqrt'],
                     'Regressor__min_samples_leaf': [1, 2, 4],
                     'Regressor__min_samples_split': [2, 5, 10],
                     }

    # Parametri di Tuning del nostro RFR
    grid_pipeline = GridSearchCV(estimator=pipe_RFR,
                                 param_grid=CV_parameters,
                                 cv=3,
                                 n_jobs=-1, )
    grid_pipeline.fit(X_train, y_train)
    y_RF_pred = grid_pipeline.predict(X_test)
    print("Random forest r2_score = ", r2_score(y_test, y_RF_pred))
    return pipe_RFR

########### CLASSIFICAZIONE CIRCOSCRIZIONI ##############
def circoscrizione_attiva(link):
    """
    Funzione che prende il dataframe raffinato dei tweets e determina per ogni giornata
    la circoscrizione con più tweets
    Ritorna una lista lunga 61 con i nomi delle circoscrizioni con più tweets per quel giorno.
    I dati vengono già encodati dalla funzione One_Hot_Featuere.
    """
    tw=pd.read_csv(link)

    tw.dropna(subset=["circoscrizione"], inplace=True)
    tw.reset_index(inplace=True)

    temp=tw.groupby(["month", "day","circoscrizione"]).size()
    maxi=temp.groupby(["month", "day"]).idxmax()

    output=[i[2] for i in maxi]
    print(output)
    return output

def One_Hot_feature(data, feature):
    """
    Funzione che prende in Input un DF in cui c'è una feature categorica e che restituisce il DF stesso senza la colonna
    categorica e con le colonne encodate.
    L'encoding è rappresentato come varie colonne per le varie categorie, dove ci sono dati 1 -> appartiene alla classe
    0 -> non appartiene alla classe.
    Feature si riferisce al nome della colonna del DF di riferimento e va passato come stringa.
    """
    le_feat = LabelEncoder()
    data[feature + '_encoded'] = le_feat.fit_transform(data[feature])
    enc = OneHotEncoder()
    X = enc.fit_transform(data[feature + '_encoded'].values.reshape(-1, 1)).toarray()
    dfOneHot = pd.DataFrame(X, columns=[feature + str(int(i) + 1) for i in range(X.shape[1])])
    data = pd.concat([data, dfOneHot], axis=1)
    data.drop(columns=['Weekday','weekday_encoded'], inplace=True)
    return data





def Random_Forest_Classifier_Circoscrizione(data):
    """
    La funzione inizialmente inizia importando i dati ed eliminando le prime due giornate, poichè mancano i dati storici
    per effettuare una predizione di qualsiasi tipo.
    In seguito i dati vengono Encodati dalla funzione custom One_Hot_feature, per poi essere gettati dentro alla
    pipeline di apprendimento su cui viene fatta una cross validation.
    La funzione printa il risultato di un'accuracy score e restituisce il modello migliore già fittato per ulteriori usi.
    """
    # creo il vettore delle y trovando qual è la circoscrizione più attiva, i dati sono già encoded
    target = circoscrizione_attiva(data_path_out / "twitter_final.csv")
    target = pd.Series(target)
    target.drop([target.index[0], target.index[1]], inplace=True)
    # vedere se funziona altrimenti aggiungere una funzione ad hoc per le serie
    target = One_Hot_feature(target, 'circoscrizione')

    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3)    # abbiamo pochissimi record per valori maggiori di 0.3

    #pipeline
    pipe_RFC = Pipeline([
        ('scaler', StandardScaler()),
        ('Regressor', RandomForestClassifier(bootstrap=False))
    ])

    # Grid search CV
    CV_parameters = {'Regressor__n_estimators': [50, 100, 200, 500],    # Valori superiori rallentano l'algoritmo
                     'Regressor__max_depth': [5, 10, 20, 50, 70, 100],  # Rasoio di Occam per evitare overfitting
                     'Regressor__min_samples_leaf': [1, 2, 4],          # Sempre rasoio di Occam
                     'Regressor__min_samples_split': [2, 5, 10, 15, 20],
                     }

    RFC_CV = GridSearchCV(estimator=pipe_RFC,
                          param_grid=CV_parameters,
                          n_jobs=-1,
                          cv=2
                          )

    RFC_CV.fit(X_train, y_train)
    y_RFC_pred = RFC_CV.predict(X_test)
    print("Lo score della nostra Random Forest risulta essere:", accuracy_score(y_test, y_RFC_pred), 'per il riconoscimento delle circoscrizioni più attive')
    post_analysis_classifier(predictor=RFC_CV, data=data, y=target)
    return RFC_CV

def post_analysis_classifier(predictor, data, y):
    """
    Assumiamo un Ansatz molto forte, ovvero che le circoscrizioni di Piedicastello-Centro e Oltrefersina siano le uniche
    due che effettivamente ambiscono ad essere quelle dove si twitta di più (ciò è ovviamente legato al numero di
    residenti). Possiamo quindi tracciare la ROC curve e la precision-recall curve, plottare la confusion matrix.
    Ciò aiuta effettivamente a contestualizzare lo score decentemente alto che abbiamo avuto.
    best_pred è il miglior predittore trovato (solitamente tramite CV) e y_pred è la predizione fatta sull'insieme di
    test.
    """
    comparison = (y_pred == y_test)
    plot_precision_recall_curve(estimator=predictor, X=data, y=y)
    plot_roc_curve(estimator=predictor, X=data, y=y)
    plot_confusion_matrix(estimator=predictor, X=data, y=y)

