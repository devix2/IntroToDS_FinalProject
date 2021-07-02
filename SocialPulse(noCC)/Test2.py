import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import EDA


from functions import *


#Importiamo il database dei tweets

df=pd.read_csv("data/processed/twitter_final.csv")
df=gpd.GeoDataFrame(df)   #Usare diretto Geopandas crasha il kernel...

#col_list = list(df)
#col_list[6], col_list[5] = col_list[5], col_list[6]

df




NightP=EDA.Nightingale_Plot(df["hours"])


 # Generate html document
NightP.render('Test.html')