# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:58:18 2013

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
from pydap.client import open_url

urlname=open("ctrl_uvmodel.csv", "r").readlines()[0][27:-1]
depth=int(open("ctrl_uvmodel.csv", "r").readlines()[1][22:-1])
TIME=open("ctrl_uvmodel.csv", "r").readlines()[2][31:-1]
print 'first'
def sh_bindata(x, y, z, xbins, ybins):
    ix=np.digitize(x,xbins)
    iy=np.digitize(y,ybins)
    xb=0.5*(xbins[:-1]+xbins[1:]) # bin x centers
    yb=0.5*(ybins[:-1]+ybins[1:]) # bin y centers
    zb_mean=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    for iix in range(1,len(xbins)):
        for iiy in range(1,len(ybins)):
            k,=np.where((ix==iix) & (iy==iiy))
            zb_mean[iix-1,iiy-1]=np.mean(z[k])
    return xb,yb,zb_mean

if urlname=="massbay":
    TIME=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S") 
    now=dt.datetime.now()
    if TIME>now:
         diff=(TIME-now).days
    else:
         diff=(now-TIME).days
    if diff>3:
        print "please check your input start time,within 3 days both side form now on"
        sys.exit(0)   
print urlname
if urlname=="30yr":
      stime=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
      timesnum=stime.year-1981
      standardtime=dt.datetime.strptime(str(stime.year)+'-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
      timedeltaprocess=(stime-standardtime).days
      startrecord=26340+35112*(timesnum/4)+8772*(timesnum%4)+1+timedeltaprocess*24     
      url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?lon,lat,lonc,latc,time,nv,h,siglay,v,u'
else:
    timeperiod=(TIME)-(now-timedelta(days=3))
    startrecord=(timeperiod.seconds)/60/60
    url='http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_FVCOM_OCEAN_MASSBAY_FORECAST.nc?lon,lat,lonc,latc,time,nv,h,siglay,v,u'
print startrecord
nc = netCDF4.Dataset(url)
print "hold on readin nc"
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
latc = nc.variables['latc'][:]
lonc = nc.variables['lonc'][:]
h = nc.variables['h'][:]
siglay=nc.variables['siglay']
u= nc.variables['u']
v= nc.variables['v']
nv = nc.variables['nv'][:].T - 1
utotal=[]
vtotal=[]
for i in range(len(lon)):
    depthtotal=siglay[:,i]*h[i]
    layer=np.argmin(abs(depthtotal+depth))
    print i,layer
    utotal.append(u[startrecord,layer,i])
    vtotal.append(v[startrecord,layer,i])
utotal=np.array(utotal)
vtotal=np.array(vtotal)
xi = np.arange(min(lon)-0.1,max(lon)+0.1,0.5)
yi = np.arange(min(lat)-0.1,max(lat)+0.1,0.25)
xb,yb,ub_mean = sh_bindata(lon[::-1], lat[::-1], utotal, xi, yi)
xb,yb,vb_mean = sh_bindata(lon[::-1], lat[::-1], vtotal, xi, yi)
xxb,yyb = np.meshgrid(xb, yb)
latsize=[min(lat)-0.6,max(lat)+0.6]
lonsize=[min(lon)-0.6,max(lon)+0.6]
plt.figure()
m = Basemap(projection='cyl',llcrnrlat=min(latsize),urcrnrlat=max(latsize),\
            llcrnrlon=min(lonsize),urcrnrlon=max(lonsize),resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,5),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,10),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()
ub = np.ma.array(ub_mean, mask=np.isnan(ub_mean))
vb = np.ma.array(vb_mean, mask=np.isnan(vb_mean))
Q=m.quiver(xxb,yyb,ub,vb,scale=10)

plt.quiverkey(Q,0.8,0.05,1, '1m/s', labelpos='W')
plt.title(urlname+' model map track Depth:'+str(depth)+' Time:'+str(TIME)) 
plt.savefig(urlname+'_modelmaptrack'+str(TIME)+'.png')
