import pandas as pd
import numpy as np

data = pd.DataFrame()
data = pd.read_csv("AIS_2020_01_01.csv")


data.drop(['Length','Width','Draft','Cargo','Status','TransceiverClass'], inplace = True, axis =1) #Removendo colunas inuteis
data.dropna() # removendo valores faltantes '?'


def exportVesselName(data): #Função para exportar todos os nomes de barcos do dataset, exporta apenas 1 nome de cada.
    name_list =[]
    name_list.append(data['VesselName'][0])

    for i in range(data.shape[0]):
        if(data['VesselName'][i] not in name_list):
            name_list.append(data['VesselName'][i])

    df = pd.DataFrame(name_list)
    return df.to_csv("VesselNames.csv", index= False)

def exportcords(): # função que le a lista de nomes e exporta cada DataFrame dos nomes em um arquivo .csv
    v_names =  pd.read_csv("VesselNames.csv")
    v_names.drop([0], inplace = True, axis = 0)
    data_sort = data.sort_values('BaseDateTime')  # Ordenando a coluna tempo.

    for i in range(1,v_names.shape[0]):
        data_sort.loc[data_sort['VesselName'] == v_names.iloc[i,-1]].to_csv("Vessel/" +v_names.iloc[i,-1] +".csv", index = False)


exportcords()
