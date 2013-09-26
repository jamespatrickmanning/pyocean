# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:38:59 2013

@author: jmanning
"""
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from datetime import datetime
from pydap.client import open_url
def nearlonlat(lon,lat,lonp,latp):
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    #dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    #min_dist=np.sqrt(dist2[i])
    return i#,min_dist 
TIME="1985-6-17 23:49:00"
numdays=1
depth=-1
FN='XY.npz'
Z=np.load(FN)
x=Z['X']
y=Z['Y']
stime=datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
timesnum=stime.year-1981
standardtime=datetime.strptime(str(stime.year)+'-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
timedeltaprocess=(stime-standardtime).days
startrecord=26340+35112*(timesnum/4)+8772*(timesnum%4)+1+timedeltaprocess*24+stime.hour
endrecord=startrecord+24*numdays
######read-in map#########
url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'lon,lat,latc,lonc,siglay,h,Times['+str(startrecord)+':1:'+str(startrecord)+']'
dataset = open_url(url)
latc = np.array(dataset['latc'])
lonc = np.array(dataset['lonc'])
lat = np.array(dataset['lat'])
lon = np.array(dataset['lon'])
siglay=np.array(dataset['siglay'])
h=np.array(dataset['h'])
latsize=[34,48]
lonsize=[-73,-60]
fig=plt.figure(figsize=(7,6))
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,1),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,1),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()
#m.plot(lon,lat,'r.',lonc,latc,'b+')
lo=-67.28
la=41.35
latd,lond=[],[]
kf=nearlonlat(lonc,latc,lo,la) # nearest triangle center F - face
kv=nearlonlat(lon,lat,lo,la)
depthtotal=siglay[:,kv]*h[kv]
layer=np.argmin(abs(depthtotal-depth))
for i in range(startrecord,endrecord):
############read the particular time model from website#########    
    timeurl='['+str(i)+':1:'+str(i)+']'
    uvposition=str([layer])+str([kf])
    url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'Times'+timeurl+',u'+timeurl+uvposition+','+'v'+timeurl+uvposition 
    dataset = open_url(url)
    u=np.array(dataset['u'])
    v=np.array(dataset['v'])
    print kf,u[0,0,0],v[0,0,0],layer
    par_u=u[0,0,0]
    par_v=v[0,0,0]   
    xdelta=par_u*60*60
    ydelta=par_v*60*60
    latdelta=ydelta/111111
    londelta=(xdelta/(111111*np.cos(la*np.pi/180)))
    la=la+latdelta
    lo=lo+londelta
    latd.append(la)
    lond.append(lo)
    m.plot(lond,latd,linewidth=1.5,color='r')
for nn in range(1,5):
    for n in range(0,20):
        lo=x[n,nn]
        la=y[n,nn]
        print n,nn,lo,la
        latd,lond=[],[]
        kf=nearlonlat(lonc,latc,lo,la) # nearest triangle center F - face
        kv=nearlonlat(lon,lat,lo,la)
        depthtotal=siglay[:,kv]*h[kv]
        layer=np.argmin(abs(depthtotal-depth))
        for i in range(startrecord,endrecord):
############read the particular time model from website#########    
               timeurl='['+str(i)+':1:'+str(i)+']'
               uvposition=str([layer])+str([kf])
               url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'Times'+timeurl+',u'+timeurl+uvposition+','+'v'+timeurl+uvposition 
                
               dataset = open_url(url)
               u=np.array(dataset['u'])
               v=np.array(dataset['v'])  
################get the point according the position###################
               print kf,u[0,0,0],v[0,0,0],layer
               par_u=u[0,0,0]
               par_v=v[0,0,0]   
               xdelta=par_u*60*60
               ydelta=par_v*60*60
               latdelta=ydelta/111111
               londelta=(xdelta/(111111*np.cos(la*np.pi/180)))
               la=la+latdelta
               lo=lo+londelta
               latd.append(la)
               lond.append(lo)
               kf=nearlonlat(lonc,latc,lo,la) # nearest triangle center F - face
               kv=nearlonlat(lon,lat,lo,la)# nearest triangle vertex V - vertex 
               depthtotal=siglay[:,kv]*h[kv]
               layer=np.argmin(abs(depthtotal-depth))
        m.plot(lond,latd,linewidth=1.5,color='r')
        plt.show()