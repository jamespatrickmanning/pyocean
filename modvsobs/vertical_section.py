# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:48:11 2015

@author: zhaobin
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import netCDF4
from matplotlib.mlab import griddata
import sys
sys.path.append('../modules')
import basemap
from basemap import basemap_usgs,basemap_standard
from turtleModule import dist,str2ndlist
   
def getFVcom(latpt,lonpt,time_roms):
    url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
    nc = netCDF4.Dataset(url)
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    Depth = nc.variables['h'][:]
    siglay=nc.variables['siglay'][:]
    time=nc.variables['time'][:]
    modtemp=nc.variables['temp'] 
    modtime=[]
    for i in range(len(time)):
        t=timedelta(days=float(time[i])).total_seconds()
        modtime.append(t)                        #change time days to seconds
    depth=(-Depth*siglay).transpose()                #each layer`s depth
    distance=dist(lonpt,latpt,lon,lat)
    node=np.argmin(distance)                 #get nearest node
    t_diff=(time_roms-datetime(1858,11,17)).total_seconds()     #1858,11,17 is FVCOM`s start time
    TIME=np.argmin(abs(t_diff-np.array(modtime)))
    Temp=[]
    for i in range(45):
        t=modtemp[TIME][i][node]
        Temp.append(t)
    return Temp,depth[node],Depth[node]
#########################################################
lat_AB01=42.0368
lon_AB01=-70.1313                       #location of AB01
lat=np.arange(42.0368,41.7797,-0.025)
lon=np.arange(-70.1313,-70.4873,-0.035)  #location of vertical transect

time=[datetime(2004,9,19),datetime(2004,9,25)]   #choose two days
distance_AB01=dist(lon[0],lat[0],lon_AB01,lat_AB01)
fig = plt.figure()
for q in range(len(time)):
    Temp,depth,deepest=[],[],[]
    for i in range(len(lat)):
        t,d,D=getFVcom(lat[i],lon[i],time[q])
        depth.append(d)
        deepest.append(D)
        Temp.append(t)
    distance=list(np.array([dist(lon[0],lat[0],lon[-1],lat[-1])])/len(lat)*range(0,len(lat)))   #this is distance between location       
    distances=[]
    for i in range(45):
        distances.append(distance)
    dd=np.array(distances).transpose()
    TEMP,DEPTH,DIST=[],[],[]
    for i in range(len(Temp)):
        for j in range(len(Temp[0])):
            TEMP.append(Temp[i][j])
            DEPTH.append(depth[i][j])
            DIST.append(dd[i][j])
    dis_i = np.linspace(0,distance[-1],1000)
    dep_i = np.linspace(max(DEPTH),0,1000) 
    modtemp_i = griddata(np.array(DIST),np.array(DEPTH),np.array(TEMP),dis_i,dep_i)
    ax = fig.add_subplot(1,2,q+1)
    CS = ax.contourf(dis_i, dep_i, modtemp_i, np.arange(8,18,0.5), cmap=plt.cm.rainbow,
                  vmax=abs(modtemp_i).max(), vmin=-abs(modtemp_i).max())     
    ax.plot(distance,deepest)
    polygon=[]
    for j in range(len(deepest)):
       polygon.append([distance[j],deepest[j]])
    polygon.append([distance[-1],max(deepest)+1])
    polygon.append([distance[0],max(deepest)+1])       #plot white when it is solid
    pg=plt.Polygon(polygon,color='white')  
    ax.add_patch(pg)
    depth_AB01=deepest[np.argmin(abs(distance_AB01-np.array(distance)))]
    plt.scatter(distance_AB01,depth_AB01)
    plt.annotate('AB01',xy=(distance_AB01,depth_AB01),xytext=(distance_AB01+1,depth_AB01+1),arrowprops=dict(frac=0.3,facecolor='red', shrink=0.2))
    plt.ylim([max(deepest)+1,0])
    plt.xlim([min(distance),max(distance)])
    plt.title(str(time[q].date()),fontsize=20)
    cbar=plt.colorbar(CS)
    cbar.ax.tick_params(labelsize=15)
plt.show()
'''
latsize=[41.,42.5]
lonsize=[-71.,-70.1]
bathy=True
draw_parallels=True
parallels_interval=[0.5]
cont_range=[-200,-100]
ss=10
basemap_usgs(latsize,lonsize,bathy,draw_parallels,parallels_interval,cont_range,ss)
basemap_standard(latsize,lonsize,[2])
plt.scatter(lon,lat,20,marker='o',color='r')
plt.scatter(lon_AB01,lat_AB01,10,marker='o',color='b')
plt.annotate('AB01',xy=(lon_AB01,lat_AB01),xytext=(lon_AB01,lat_AB01+0.1),arrowprops=dict(frac=0.3,shrink=0.25,facecolor='blue'))
plt.show()
'''