import numpy as np 
import pandas as pd 
import requests 
import json
import os

traffic_dat = pd.read_csv('trafficDAT.csv')

garmon_dat = pd.read_csv('../datathon_data/garmon_0217.csv')

def setPeak(hour):
    if hour <= 10 or hour >= 15:
        return("Peak")
    else:
        return("Slow")

garmon_dat['DATEUTC'] = pd.to_datetime(garmon_dat['DATEUTC'])

garmon_dat['period'] = garmon_dat['DATEUTC'].map(lambda x: setPeak(x.hour))
garmon_dat['date'] = garmon_dat['DATEUTC'].dt.date

agg_dict = {'LAT':'first', 'LON':'first', 'ALT':'first', 
'TEMPC':'mean', 'HUMIDITY':'mean', 'WINDCHILLF':'mean', 'WINDSPEEDKMH':'mean'}

garmon_dat = garmon_dat.groupby(['ID', 'date', 'period']).agg(agg_dict).reset_index()

garmon_dat.to_csv('garmonOUT.csv', index='False')

garmon_dat = pd.read_csv('garmonOUT.csv')

garmon_gps = garmon_dat[['ID', 'LAT', 'LON']].drop_duplicates()

## Build dictionary of id:dist for each segment
traffic_gps = traffic_dat[['segment_id', 'lng', 'lat']].drop_duplicates()

def compute_sqeucl(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2

segment_distD = {}

n = traffic_gps.shape[0]

garmon_ids = np.array(garmon_gps[['ID']]).ravel()

for i in range(n):
    current_arr = traffic_gps.iloc[i]
    segment = current_arr[0]
    current_lng = current_arr[1]
    current_lat = current_arr[2]

    distances = garmon_gps[['LAT', 'LON']].apply(lambda x:\
         compute_sqeucl(x[0], x[1], current_lat, current_lng), axis=1)
    distances = np.array(distances).ravel()

    dist_dict = {x:y for x, y in zip(garmon_ids, distances)}

    segment_distD.update({int(segment):dist_dict})


## Append to the traffic data the weighted mean of the weather covariates
weather_columns = pd.DataFrame()
n = traffic_dat.shape[0]

for i in range(n):
    print(str(i/n))
    traffic_current = traffic_dat.iloc[i]
    date_current = traffic_current['date']
    period_current = traffic_current['period']
    segment_current = traffic_current['segment_id']

    garmon_sub = garmon_dat[(garmon_dat.date.astype('str') == date_current) & (garmon_dat.period == period_current)]
    dist_sub = pd.DataFrame({'ID':list(segment_distD[segment_current].keys()),
                             'Dist':list(segment_distD[segment_current].values())})
    
    garmon_sub = garmon_sub.merge(dist_sub)
    
    wghts = 1/np.array(garmon_sub['Dist'])
    c = np.sum(wghts)
    garmon_variates = garmon_sub[['ALT', 'TEMPC', 'HUMIDITY', 'WINDCHILLF', 'WINDSPEEDKMH']]
    
    agg_variates = garmon_variates.apply(lambda x: np.sum(x*wghts/c))
    agg_variates = np.array(agg_variates).ravel()
    cols = ['ALT', 'TEMPC', 'HUMIDITY', 'WINDCHILLF', 'WINDSPEEDKMH']
    
    if garmon_sub.shape[0] > 0:
        row_dict = pd.DataFrame(agg_variates.reshape(1, -1))
        row_dict.columns = cols
    else:
         row_dict = pd.DataFrame(np.repeat(None, len(cols)).reshape(1, -1))
         row_dict.columns = cols
    
    weather_columns = pd.concat((weather_columns, row_dict), axis=0)
    

weather_columns.to_csv('weatherCOLS.csv', index=False)

weather_columns = weather_columns.reset_index()
weather_columns = weather_columns.drop('index', axis=1)

tw_dat = pd.concat((traffic_dat, weather_columns), axis=1)

tw_dat.to_csv('trafficWeather_dat.csv', index=False)