import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import os

local_path = '/home/marc/School/datathon_data'

os.listdir(local_path)

la19_dat = pd.read_csv(local_path + '/leuvenair_2019.csv')
la18_dat = pd.read_csv(local_path + '/leuvenair_2018.csv')
la20_dat = pd.read_csv(local_path + '/leuvenair_2020.csv')

keep_cols = ['LAT', 'LON', 'SDS011ID']

all_dat = [la19_dat, la18_dat, la20_dat]

map_dat = pd.DataFrame()

for d in all_dat:
    d = d.groupby(d.SDS011ID).agg({'LAT':'first', 'LON':'first'})
    map_dat = pd.concat((map_dat, d), axis=0)

map_dat = map_dat.reset_index()

map_dat = map_dat.groupby(map_dat.SDS011ID).agg({'LAT':'first', 'LON':'first'})

map_dat = map_dat.reset_index()

map_dat.to_csv('airsensor_coordinates.csv')

## Check positions of sensors on map
import mplleaflet

plt.plot(map_dat['LON'], map_dat['LAT'], 'p')
mplleaflet.show()
        


