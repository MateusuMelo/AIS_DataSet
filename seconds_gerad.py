from datetime import timedelta , datetime
import pandas as pd

data = pd.read_csv("Vessel_byIMO/IMO0000000.csv")

for i in range (len(data)):
    time = datetime.strptime(data['BaseDateTime'][i], "%Y-%m-%dT%H:%M:%S")
    data.loc[i,'segundos'] = time.timestamp()
    print((i*100)/len(data))

data.head()
