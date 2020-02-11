import requests 
import pandas as pd 
import numpy as np 

request = requests.get('https://telraam-api.net/v0/cameras')

r_json = request.json()

## Some camera are problematic