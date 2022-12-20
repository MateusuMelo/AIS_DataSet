import numpy as np
import pandas as pd
from datetime import timedelta , datetime
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

# Ais data pode ser encontrado nesse link https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2022/
def load_data(path):
    data = pd.DataFrame()
    data = pd.read_csv(path) #arquivo AIS bruto .csv
    data.drop(['Length','Width','Draft','Cargo','Status','TransceiverClass'], inplace = True, axis =1) #Removendo colunas inuteis
    data.dropna() # removendo valores faltantes '?'
    return data


def exportar_IMOs(data): #Função para exportar todos os sinais de barcos do dataset, exporta apenas 1 sinal de cada.
    name_list =[]
    name_list.append(data['IMO'][0])

    for i in range(data.shape[0]):
        if(data['IMO'][i] not in name_list):
            name_list.append(data['IMO'][i])

    df = pd.DataFrame(name_list)
    return df.to_csv("IMO.csv", index= False)

def exportar_cordenadas(data): # função que le a lista sinais e exporta cada DataFrame dos sinais em um arquivo .csv
    v_sign =  pd.read_csv("IMO.csv")
    v_sign.drop([0], inplace = True, axis = 0)


    for i in range(1,v_sign.shape[0]):
        data.loc[data['IMO'] == v_sign.iloc[i,-1]].to_csv("Vessel_byIMO/" +v_sign.iloc[i,-1] +".csv", index = False)

def seconds_generator(data): #função que converte coluna 'BaseDateTime em um numero inteiro.

    for i in range (len(data)):
        time = datetime.strptime(data['BaseDateTime'][i], "%Y-%m-%dT%H:%M:%S")
        data.loc[i,'segundos'] = time.timestamp()

    return data

def hour_generator(data): #função que gera horas faltantes entre os intervalos fornecidos.

    data_sort = data.sort_values('BaseDateTime',ignore_index=True)
    time = datetime.strptime(data_sort['BaseDateTime'][0],"%Y-%m-%dT%H:%M:%S")
    print(time.strftime("%Y-%m-%dT%H:%M:%S"))
    last = data['BaseDateTime'][len(data_sort)- 1]
    print(last)

    while  time.strftime("%Y-%m-%dT%H:%M:%S") != last:
        data_sort = data_sort.append({'BaseDateTime':time.strftime("%Y-%m-%dT%H:%M:%S")}, ignore_index=True)
        time = time + timedelta(seconds=1)
        print(time)


    data_sort = data_sort.sort_values('BaseDateTime',ignore_index=True)
    data_sort['MMSI'] = data['MMSI'][0]
    data_sort['VesselName'] = data['VesselName'][0]
    data_sort['IMO'] = data['IMO'][0]
    data_sort['CallSign'] = data['CallSign'][0]
    data_sort['VesselType'] = data['VesselType'][0]
    data_sort = seconds_generator(data_sort)

    return data_sort.to_csv(data_sort['IMO'][0] + "_H.csv",ignore_index = True)

def knnimputer(data_train, data_test,n): #função que implementa o previsor sendo data_train os daos originais e data_test os dados a serem previstos.
    #data_train = pd.DataFrame()
    #data_train = pd.read_csv(path)
    #data_test = pd.read_csv("Predict/"+path)

    data_test.sort_values('BaseDateTime')
    data_test.drop(['LAT','LON','Heading'],inplace = True, axis =1)
    data_train.sort_values('BaseDateTime')


    Knn_lat = KNeighborsRegressor(n_neighbors=n, weights='distance', metric='euclidean')  # sepa que deu certo
    Knn_lat.fit(data_train[['segundos']], data_train[['LAT']])

    Knn_lon = KNeighborsRegressor(n_neighbors=7, weights='distance', metric="euclidean")
    Knn_lon.fit(data_train[['segundos']], data_train[['LON']])

    Knn_heading = KNeighborsRegressor(n_neighbors=n, weights='distance', metric="euclidean")
    Knn_heading.fit(data_train[['segundos']], data_train[['Heading']])

    data_test['LAT'] = Knn_lat.predict(data_test[['segundos']])


    data_test['LON'] = Knn_lon.predict(data_test[['segundos']])
    data_test['Heading'] = Knn_heading.predict(data_test[['segundos']])

    data_test.to_csv(data_test['IMO'][0] + "_knn.csv", index= False)
    return data_test

def grafico(x, y): #função gera um grafico de comparação dos valores fornecidos e os valores previstos.

    fig,axs = plt.subplots(2)
    axs[0].scatter(x['segundos'],x['LAT'],)
    axs[1].scatter(y['segundos'], y['LAT'])
    plt.show()

def prever(path):
    data = pd.read_csv(path)
    data =seconds_generator(data)
    hour_generator(data)
    data_h = pd.read_csv(data['IMO'] + "_H.csv")


    data_treinado = knnimputer(data,data_h,5)

    grafico(data_h,data_treinado)

prever("Vessel_byIMO/IMO0000000.csv")