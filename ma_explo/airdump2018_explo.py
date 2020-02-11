import pandas as pd 
import numpy as np 
import os
import matplotlib.pyplot as plt

os.chdir('d:/MarcandreC/Desktop/Datathon_2020/Exploration')
os.listdir('../')


lair18_dat = pd.read_csv('../LEUVENAIRfulldump2018.csv')

sds1_dat = lair18_dat.loc[lair18_dat.SDS011ID == 6561, :]

sds1_dat['DATEUTC'] = pd.to_datetime(sds1_dat.DATEUTC)

times = sds1_dat.DATEUTC.map(lambda x: (x.year, x.month, x.day, x.hour))

agg_dict = {
    'LAT':'first', 
    'LON':'first',
    'SDS011ID':'first',
    'PM2.5':'mean'}

sds1_dat = sds1_dat.groupby(times).agg(agg_dict)

sds1_series = sds1_dat['PM2.5']

sds1_series.index = sds1_series.index.map(
    lambda x: '{0}-{1}-{2} {3}:0:0'.format(x[0], x[1], x[2], x[3])
)   

sds1_series.index = pd.to_datetime(sds1_series.index)

sds1_series.plot()
