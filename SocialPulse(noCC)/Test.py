
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import Point, Polygon


from functions import *
import make_dataset as m_d



a=m_d.df_reg()
print(a)