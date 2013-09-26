# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:48:40 2013

@author: jmanning
"""
from conversions import ll2uv
from datetime import datetime as dt
from matplotlib.dates import date2num

lat=[40.0,40.05,40.15,40.35]
lon=[70.,70.,70.,70.]
year=2013
datet=[dt(year,1,1,0,0,0),dt(year,1,2,0,0,0),dt(year,1,3,0,0,0),dt(year,1,4,0,0,0)]

yearday=list(date2num(datet)-date2num(dt(year,1,1,0,0,0)))
[u,v,spd,jdn]=ll2uv(yearday,lat,lon)
print spd