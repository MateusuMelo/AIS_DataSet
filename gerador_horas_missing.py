import pandas as pd
from datetime import timedelta ,datetime


def hour_generator(path):
    data = pd.DataFrame()
    data = pd.read_csv("@path")

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

    return data_sort.to_csv("@path", index=False)

def seconds_generator(data):

    for i in range (len(data)):
        time = datetime.strptime(data['BaseDateTime'][i], "%Y-%m-%dT%H:%M:%S")
        data.loc[i,'segundos'] = time.timestamp()

    return data

data = pd.read_csv("Vessel/C6UI8.csv")
seconds_generator(data)

data.to_csv("Vessel/C6UI8.csv",index=False)