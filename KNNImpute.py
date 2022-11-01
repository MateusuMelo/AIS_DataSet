import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.metrics.pairwise import nan_euclidean_distances, euclidean_distances
from sklearn.neighbors import KNeighborsRegressor
from datetime import timedelta , datetime
from sklearn.impute import SimpleImputer

data_set = pd.DataFrame()
data_set = pd.read_csv("Vessel/C6UI8.csv",)
data_pred = pd.read_csv("Predict/Vessel/C6UI8.csv")
data_pred.sort_values('BaseDateTime')

data_set.sort_values('BaseDateTime')
data_filtrado = data_set.dropna()
data_train = data_filtrado[['LAT']].to_numpy()
data_train_y = data_filtrado[['LON']].to_numpy()


Knn_lat = KNeighborsRegressor(n_neighbors=20,weights='distance',metric="minkowski") #sepa que deu certo
Knn_lat.fit( data_set[['segundos']],data_set[['LAT']])

Knn_lon = KNeighborsRegressor(n_neighbors=20, weights='distance', metric="minkowski")
Knn_lon.fit( data_set[['segundos']],data_set[['LON']])

Knn_heading =  KNeighborsRegressor(n_neighbors=20,weights='distance',metric="minkowski")
Knn_heading.fit( data_set[['segundos']],data_set[['Heading']])

ffit = KNeighborsRegressor(n_neighbors=20,weights='distance',metric="minkowski")
ffit.fit( data_set[['segundos']],data_set[['LAT']])



data_pred['LAT'] = ffit.predict(data_pred[['segundos']])
data_pred['LON'] = Knn_lon.predict(data_pred[['segundos']])
data_pred['Heading'] = Knn_heading.predict(data_pred[['segundos']])
data_pred.to_csv("Predict/C6UI8_previsto.csv")

