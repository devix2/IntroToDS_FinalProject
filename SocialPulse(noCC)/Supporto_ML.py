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
from sklearn.model_selection import train_test_split

# custom lib
# import make_dataset as m_d


def logistic_regressor_fittato(X,y, time):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    pipe_logistic = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        ('scaler', StandardScaler()),
        ('regressor', LogisticRegression())
    ])

    pipe_logistic = pipe_logistic.fit(X_train, y_train)
    y_logistic_pred = pipe_logistic.predict(X_test)
    print("Logistic regression r2_score =", r2_score(y_test, y_logistic_pred), 'per la ', time)
    return pipe_logistic




############### Random Forest Regressor ###############
def Random_Forest_Regressor_CV(X,y, time):
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
    print("Random forest r2_score = ", r2_score(y_test, y_RF_pred), 'per la ', time)

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
    print("Random forest r2_score = ", r2_score(y_test, y_RF_pred), 'per la ', time)
    return pipe_RFR

######## CLASSIFICAZIONE CIRCOSCRIZIONI ##############
def circoscrizione_attiva(link):
    tw=pd.read_csv(link)

    tw.dropna(subset=["circoscrizione"], inplace=True)
    tw.reset_index(inplace=True)

    temp=tw.groupby(["month", "day","circoscrizione"]).size()
    maxi=temp.groupby(["month", "day"]).idxmax()

    output=[i[2] for i in maxi]
    print(output)
    return output



def Random_Forest_Classifier_Circoscrizione(data):
    # creo il vettore delle y trovando qual è la circoscrizione più attiva
    target = circoscrizione_attiva("data/processed/twitter_final.csv")
    target = pd.Series(target)
    target.drop([target.index[0], target.index[1]], inplace=True)
    enc = OneHotEncoder(sparse=False, handle_unknown='ignore')
    target = enc.fit_transform(target.values[:,None])

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.4)

    pipe_RFC = Pipeline([
        #('encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),
        ('scaler', StandardScaler()),
        ('Regressor', RandomForestClassifier(bootstrap=False))
    ])

    # Provo con una grid search CV
    # Questa griglia va ricontrollata
    CV_parameters = {'Regressor__n_estimators': [5, 10, 25, 50],
                     'Regressor__max_depth': [10, 20, 50, 70, 100, None],
                     'Regressor__max_features': ['auto', 'sqrt'],
                     'Regressor__min_samples_leaf': [1, 2, 4],
                     'Regressor__min_samples_split': [2, 5, 10],
                     }
    # Parametri di Tuning del nostro RFR
    RFC_CV = GridSearchCV(estimator=pipe_RFC,
                          param_grid=CV_parameters,
                          n_jobs=-1,
                          cv=3
                          )
    RFC_CV.fit(X_train, y_train)
    y_RFC_pred = RFC_CV.predict(X_test)
    print("Lo score della nostra Random Forest risulta essere:", r2_score(y_test, y_RFC_pred), 'per il riconoscimento delle circoscrizioni più attive')
