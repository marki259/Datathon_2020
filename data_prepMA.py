import numpy as np 
import pandas as pd 
import requests 
import json

## Get list of segments
segments = requests.get("https://telraam-api.net/v0/segments/active")
print(segments.status_code)

segment_ids = []
for segment in segments.json()['features']:
    segment_ids.append(segment['properties']['id'])

segment_ids = np.unique(segment_ids)

## Working on intake
def gen_time(year, month, day, hour):
    if month < 10:
        month = '0' + str(month)
    if day < 10: 
        day = '0' + str(day)
    if hour < 10: 
        hour = '0' + str(hour)

    date = str(year) + '-' + str(month) + '-' + str(day) + ' ' +\
        str(hour) + ':00'
    return(date)

def setPeak(hour):
    if hour <= 10 or hour >= 15:
        return("Peak")
    else:
        return("Slow")

full_dat = pd.DataFrame()

## Building traffic dataset
for segment in segment_ids:
    print(str(segment))
    for month in np.arange(11, 14):
        year = 2019 + (month - 1)//12
        month = month % 12

        segment_id = segment
        url = "https://telraam-api.net/v0/reports/" + str(segment_id)

        param = {"time_start":gen_time(year, month, 1, 10), 
         "time_end":gen_time(year, month + 1, 1, 10), 
         "level":"segments",
         "format": "per-hour"}
        headers = {'Content-Type': 'application/json'}

        r = requests.request("POST", url, headers=headers,data = json.dumps(param))
        if r.status_code != 200:
            continue

        dat = r.json()['report']

        dat = pd.DataFrame(dat)
        if dat.shape[0] == 0:
            continue

        dat['date'] = pd.to_datetime(dat['date'])

        dat['period'] = dat['date'].map(lambda x: setPeak(x.hour))
        dat['date'] = dat['date'].dt.date

        dat = dat[['segment_id', 'date', 'pedestrian', 'bike', 'car', 'lorry', 'period']]

        agg_dict = {'segment_id':'first', 
        'pedestrian':'sum', 
        'bike':'sum',
        'car':'sum', 
        'lorry':'sum'}

        dat = dat.groupby(['date', 'period']).agg(agg_dict).reset_index()

        full_dat = pd.concat((full_dat, dat), axis=0)

## Export as cache
## full_dat.to_csv('trafficDAT.csv')

## Appending GPS info (Taking the mean x and y per segment)
segments_list = segments.json()['features']

n = len(segments_list)

gps_dat = pd.DataFrame()

for i in range(n):
    segmentID = segments_list[i]['properties']['id']
    seg_list = pd.DataFrame(np.array(segments_list[i]['geometry']['coordinates'])[0])
    c_dat = seg_list.apply(lambda x: np.mean(x))
    c_dat = np.array(c_dat)

    dat = pd.DataFrame({'seg':[segmentID], 'x':[c_dat[0]], 'y':[c_dat[1]]})
    gps_dat = pd.concat((gps_dat, dat), axis=0)

gps_dat = gps_dat.groupby('seg').agg({'x':'first', 'y':'first'}).reset_index()

gps_dat.columns = ['segment_id', 'lng', 'lat']

gps_dat['segment_id'] = gps_dat['segment_id'].astype('int')



full_dat['segment_id'] = full_dat['segment_id'].astype(int)

traffic_dat = full_dat.merge(gps_dat, on='segment_id')

traffic_dat.to_csv('trafficDAT.csv')