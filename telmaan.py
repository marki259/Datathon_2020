import requests
import json
import pandas as pd

r_segments = requests.get("https://telraam-api.net/v0/segments/active")

segments = r_segments.json()['features']

segments_id = [s['properties']['id'] for s in segments]

len(segments_id)

## Get n of cameras per segment 
url_base = 'https://telraam-api.net/v0/cameras/segment/'
cnt = 0

for id in segments_id:
    r = requests.get(url_base + str(id))
    c = len(r.json()['camera'])
    cnt += c
    print('Counted id: {}'.format(id))
    

## Able to get historical traffic data (up to a certain point)
body = '''
{
    "time_start": "2019-03-29 00:00",
    "time_end": "2019-04-01 23:59",
    "level": "segments",
    "format":"per-hour"
}
'''


headers = {'Content-Type': 'application/json'}

url = 'https://telraam-api.net/v0/reports/349570'

r = requests.request('POST', url, headers=headers, data=body)

r.json()