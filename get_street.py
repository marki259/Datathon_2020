import requests
import json
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

## Get ids of segments
r_segments = requests.get("https://telraam-api.net/v0/segments/active")

segments = r_segments.json()['features']

segments_id = [s['properties']['id'] for s in segments]

n = len(segments_id)

## Get geographic properties per segment
## Also creates a dataset to easily draw the segments
## on a map
geo_data = pd.DataFrame()

for s in segments:
    k = s['properties']['id']
    coords = np.array(s['geometry']['coordinates'])[0]
    m = coords.shape[0]
    c_pos = np.array([i for i in range(m)])
    c_pos = c_pos.ravel()
    keys = np.repeat(str(k), m).ravel()
    lon = coords[:, 0].ravel()
    lat = coords[:, 1].ravel()
    
    tmp_dict = {'id':keys, 'pos':c_pos, 'lon':lon, 'lat':lat}
    tmp_df = pd.DataFrame(tmp_dict)

    geo_data = pd.concat((geo_data, tmp_df), axis=0)

geo_data

## Mapping the segments
plt.plot(geo_data['lon'], geo_data['lat'], '')
