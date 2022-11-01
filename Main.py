import numpy as np
import pandas as pd
from datetime import timedelta , datetime
from sklearn.neighbors import KNeighborsRegressor
import sklearn.neighbors as sk
import matplotlib.pyplot as plt

def load_data():
    data = pd.DataFrame()
    data = pd.read_csv("AIS_2020_01_01.csv") #arquivo AIS bruto .csv


    #horas = data['BaseDateTime'].str.split('T', expand = True)[1].str.split(':', expand = True) # Separanda y/m/d T h:m:s para so h:m:s
    data.drop(['Length','Width','Draft','Cargo','Status','TransceiverClass'], inplace = True, axis =1) #Removendo colunas inuteis
    data.dropna() # removendo valores faltantes '?'
    return data


def exportVesselCallSign(): #Função para exportar todos os sinais de barcos do dataset, exporta apenas 1 sinal de cada.
    data = load_data()
    name_list =[]
    name_list.append(data['CallSign'][0])

    for i in range(data.shape[0]):
        if(data['CallSign'][i] not in name_list):
            name_list.append(data['CallSign'][i])

    df = pd.DataFrame(name_list)
    return df.to_csv("CallSigns.csv", index= False)

def exportcords(): # função que le a lista sinais e exporta cada DataFrame dos sinais em um arquivo .csv
    data = load_data()
    v_sign =  pd.read_csv("CallSigns.csv")
    v_sign.drop([0], inplace = True, axis = 0)


    for i in range(1,v_sign.shape[0]):
        data.loc[data['CallSign'] == v_sign.iloc[i,-1]].to_csv("Vessel/" +v_sign.iloc[i,-1] +".csv", index = False)

def seconds_generator(path):
    data = pd.read_csv(path)

    for i in range (len(data)):
        time = datetime.strptime(data['BaseDateTime'][i], "%Y-%m-%dT%H:%M:%S")
        data.loc[i,'segundos'] = time.timestamp()

    return data.to_csv(path,index=False)


def hour_generator(path):
    seconds_generator(path)

    data = pd.DataFrame()
    data = pd.read_csv(path)


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
    data_sort.to_csv("Predict/"+path, index=False)
    seconds_generator("Predict/"+path)

def knnimputer(path):
    data_set = pd.DataFrame()
    data_set = pd.read_csv(path)
    data_pred = pd.read_csv("Predict/"+path)

    data_pred.sort_values('BaseDateTime')
    data_pred.drop(['LAT','LON','Heading'],inplace = True, axis =1)
    data_set.sort_values('BaseDateTime')


    Knn_lat = KNeighborsRegressor(n_neighbors=7, weights='distance', metric='euclidean')  # sepa que deu certo
    Knn_lat.fit(data_set[['segundos']], data_set[['LAT']])

    Knn_lon = KNeighborsRegressor(n_neighbors=7, weights='distance', metric="euclidean")
    Knn_lon.fit(data_set[['segundos']], data_set[['LON']])

    Knn_heading = KNeighborsRegressor(n_neighbors=7, weights='distance', metric="euclidean")
    Knn_heading.fit(data_set[['segundos']], data_set[['Heading']])

    data_pred['LAT'] = Knn_lat.predict(data_pred[['segundos']])
    data_pred['LON'] = Knn_lon.predict(data_pred[['segundos']])
    data_pred['Heading'] = Knn_heading.predict(data_pred[['segundos']])
    new_path = data_pred['CallSign'][0]

    data_pred.to_csv("Predict/Knn/" + new_path + ".csv", index= False)

def grafico(path):
    data_set = pd.read_csv(path)
    data_pred = pd.read_csv("Predict/Knn/" + data_set['CallSign'][0] + ".csv")

    fig,axs = plt.subplots(2)
    axs[0].scatter(data_set['segundos'],data_set['LAT'])
    axs[1].scatter(data_pred['segundos'], data_pred['LAT'])
    plt.show()



grafico("Vessel/LAJS7.csv")