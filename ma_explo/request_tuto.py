import requests

response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")

response = requests.get("http://api.open-notify.org/astros.json")
print(response.status_code)

response.json()

import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())

parameters = {
    "lat": 40.71,
    "lon": -74
}

response = requests.get(
    "http://api.open-notify.org/iss-pass.json",
    params=parameters)

jprint(response.json())

## For loop to extract the five rise time values
risetimes = []
responses = response.json()['response']

for r in responses:
    risetimes.append(r['risetime'])

print(risetimes)

from datetime import datetime

times = []
for t in risetimes:
    times.append(datetime.fromtimestamp(t))

print(times[0])

## Getting data from lastfm
apiKey = '3fe78ae55908f6cd0e965b993a911e94'
user_agent = 'dataquest'

headers = {
    'user_agent':user_agent
}

payload = {
    'api_key':apiKey,
    'method':'chart.gettopartists',
    'format':'json'
}

r = requests.get(
    'http://ws.audioscrobbler.com/2.0/',
    headers=headers,
    params=payload)

import time    

