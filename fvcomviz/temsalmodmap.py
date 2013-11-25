# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:10:22 2013

@author: jmanning
"""

from pylab import *
from matplotlib.collections import PolyCollection
import matplotlib.tri as Tri
from mpl_toolkits.basemap import Basemap
import datetime as dt
import netCDF4
import sys
import numpy as np
from datetime import timedelta

urlname=open("ctrl_temsalmod.csv", "r").readlines()[0][27:-1]
depth=int(open("ctrl_temsalmod.csv", "r").readlines()[1][22:-1])
TIME=open("ctrl_temsalmod.csv", "r").readlines()[2][31:-1]

if urlname=="30yr":
    
    stime=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
    timesnum=stime.year-1981
    standardtime=dt.datetime.strptime(str(stime.year)+'-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
    timedeltaprocess=(stime-standardtime).days
    startrecord=26340+35112*(timesnum/4)+8772*(timesnum%4)+1+timedeltaprocess*24     
    url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?temp,lon,lat,lonc,latc,time,nv,h,siglay,salinity'
else:
    TIME=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S") 
    now=dt.datetime.now()
    if TIME>now:
         diff=(TIME-now).days
    else:
         diff=(now-TIME).days
    if diff>3:
        print "please check your input start time,within 3 days both side form now on"
        sys.exit(0)
    timeperiod=(TIME)-(now-timedelta(days=3))
    startrecord=(timeperiod.seconds)/60/60
    url="http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_FVCOM_OCEAN_MASSBAY_FORECAST.nc?temp,lon,lat,lonc,latc,time,nv,h,siglay,salinity"
    
nc = netCDF4.Dataset(url)
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
latc = nc.variables['latc'][:]
lonc = nc.variables['lonc'][:]
temp=nc.variables['temp']
sali=nc.variables["salinity"]
siglay=nc.variables['siglay']
h = nc.variables['h'][:]
# read connectivity array
nv = nc.variables['nv'][:].T - 1
time_var = nc.variables['time']

# create a triangulation object, specifying the triangle connectivity array
tri = Tri.Triangulation(lon,lat, triangles=nv)
# plot depth using tricontourf
salinity=[]
temprature=[]
for i in range(len(lon)):
    depthtotal=siglay[:,i]*h[i]
    layer=np.argmin(abs(depthtotal+depth))
    print i,layer
    temprature.append(temp[startrecord,layer,i])
    salinity.append(sali[startrecord,layer,i])
temprature=np.array(temprature)
salinity=np.array(salinity)

latsize=[min(lat)-1,max(lat)+1]
lonsize=[min(lon)-1,max(lon)+1]
fig=figure(figsize=(6,8))
ax=fig.add_subplot(211)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()
tricontourf(tri,temprature)
colorbar()
plt.title(urlname+' salinity model Depth:'+str(depth)+' Time:'+str(TIME)[0:-9]) 
ax1=fig.add_subplot(212)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()
tricontourf(tri,salinity)
colorbar()
plt.title(urlname+' salinity model Depth:'+str(depth)+' Time:'+str(TIME)[0:-9]) 
plt.show()
plt.savefig(urlname+'temp_salini.png')