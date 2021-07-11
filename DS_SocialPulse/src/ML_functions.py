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
from sklearn.metrics import matthews_corrcoef, r2_score, accuracy_score, confusion_matrix
from sklearn.metrics import plot_roc_curve, plot_precision_recall_curve, plot_confusion_matrix

from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer


# custom lib
import make_dataset as m_d

################# REGRESSIONE A NUMERO DI TWEETS #########################
#Logistic
def logistic_regressor_fittato(X,y, num_features, cat_features):
    """
    Funzione che crea, fitta, testa e ritorna una pipeline con il logistic regressor,
    con alcune caratterstiche autoevidenti da codice
    Input: X sono i dati, y i targets
        num e cat features rappresentano features numeriche e categoriche (come lista di stringhe)
    Printa il risultato dell'r2 score
    """
    X=X[num_features+cat_features]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    transf=make_column_transformer(
            (StandardScaler(), num_features),
            (OneHotEncoder(handle_unknown="ignore"), cat_features),
            remainder='drop')
    pipe_logistic = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        #('scaler', StandardScaler()),
        ('transformer', transf), 
        ('regressor', LogisticRegression())
    ])

    pipe_logistic = pipe_logistic.fit(X_train, y_train)
    y_logistic_pred = pipe_logistic.predict(X_test)
    print("Logistic regression r2_score =", r2_score(y_test, y_logistic_pred))
    return pipe_logistic




#Random forest
def Random_Forest_Regressor_CV(X,y, num_features, cat_features):
    """
    Funzione che crea, fitta, testa e ritorna una pipeline con il RF regressor,
    con alcune caratterstiche autoevidenti da codice
    Printa il risultato dell'r2 score
    """
    X=X[num_features+cat_features]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    transf=make_column_transformer(
            (StandardScaler(), num_features),
            (OneHotEncoder(handle_unknown="ignore"), cat_features),
            remainder='drop')
    pipe_RFR = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        #('scaler', StandardScaler()),
        ('transformer', transf), 
        ('Regressor', RandomForestRegressor(bootstrap=False))
    ])
    #print(tranf.onehotencoder.categories_)
    
    # Vale la pena fare un tentativo prima della CV che da un'accuracy 0
    pipe_RFR.fit(X_train, y_train)
    y_RF_pred = pipe_RFR.predict(X_test)
    """
    for i in range(len(y_RF_pred)):
        y_RF_pred[i] = int(y_RF_pred[i])"""
    print("Random forest r2_score = ", r2_score(y_test, y_RF_pred))
    
    # GRID SEARCH CV
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
    print("Random forest (gridSearchCV) r2_score = ", r2_score(y_test, y_RF_pred))
    
    return grid_pipeline


########### CLASSIFICAZIONE CIRCOSCRIZIONI ##############
def circoscrizione_attiva(link):
    """
    Funzione che prende il dataframe raffinato dei tweets e determina per ogni giornata
    la circoscrizione con più tweets
    Ritorna una lista lunga 61 con i nomi delle circoscrizioni con più tweets per quel giorno
    """
    tw=pd.read_csv(link)

    tw.dropna(subset=["circoscrizione"], inplace=True)
    tw.reset_index(inplace=True)

    temp=tw.groupby(["month", "day","circoscrizione"]).size()
    maxi=temp.groupby(["month", "day"]).idxmax()

    output=[i[2] for i in maxi]
    return output



def Random_Forest_Classifier_Circoscrizione(X, y, num_features, cat_features):
    """
    La funzione inizialmente inizia importando i dati ed eliminando le prime due giornate, poichè mancano i dati storici
    per effettuare una predizione di qualsiasi tipo.
    In seguito i dati vengono Encodati dentro alla pipeline di apprendimento su cui viene fatta una cross validation.
    La funzione printa il risultato di un'accuracy score e restituisce il modello migliore già fittato per ulteriori usi.
    """
    X=X[num_features+cat_features]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    transf=make_column_transformer(
            (StandardScaler(), num_features),
            (OneHotEncoder(handle_unknown="ignore"), cat_features),
            remainder='drop')

    pipe_RFC = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        ('transformer', transf),
        ('Regressor', RandomForestClassifier(bootstrap=False))
    ])

    # Provo con una grid search CV
    # Questa griglia va ricontrollata
    CV_parameters = {'Regressor__n_estimators': [50, 100, 200, 500],  # Valori superiori rallentano l'algoritmo
                     'Regressor__max_depth': [5, 10, 20, 50, 70, 100],  # Rasoio di Occam per evitare overfitting
                     'Regressor__min_samples_leaf': [1, 2, 4],  # Sempre rasoio di Occam
                     'Regressor__min_samples_split': [2, 5, 10, 15, 20],
                     }
    # Parametri di Tuning del nostro RFR
    RFC_CV = GridSearchCV(estimator=pipe_RFC,
                          param_grid=CV_parameters,
                          n_jobs=-1,
                          cv=2
                          )
    RFC_CV.fit(X_train, y_train)
    y_RFC_pred = RFC_CV.predict(X_test)
    #Di questo sicuro fare ROC + precision-recall
    print("Lo score della nostra Random Forest risulta essere:", accuracy_score(y_test, y_RFC_pred), 'per il riconoscimento delle circoscrizioni più attive')
    
    #Gonna leave these here, more convenient than return the test values as in return RFC_CV, (X_test, y_test)
    plot_confusion_matrix(RFC_CV, X_test, y_test)
    plot_precision_recall_curve(RFC_CV, X_test, y_test)
    plot_roc_curve(RFC_CV, X_test, y_test)


    return RFC_CV


    
    