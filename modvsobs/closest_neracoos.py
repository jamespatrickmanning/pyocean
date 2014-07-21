# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:33:13 2013

@author: jmanning
"""
import pandas as pd
import numpy as np
from getdata import getemolt_latlon
from pylab import unique
from pydap.client import open_url
import sys
def get_dataset(url):
    try:
        dataset = open_url(url)
    except:
        print 'Sorry, ' + url + 'is not available' 
        sys.exit(0)
    return dataset
def nearlonlat(lon,lat,lonp,latp):
   
    cp=np.cos(latp*np.pi/180.)
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    i=np.argmin(dist2)
    min_dist=np.sqrt(dist2[i])
    return i,min_dist 
depthunique=[]
lat=[]
lon=[]
sites=[]    
site=['BF01']     
#site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
for k in range(len(site)):
    [lati,loni,on,bd]=getemolt_latlon(site[k])
    (a,b)=divmod(float(lati),100)   
    aa=int(a)
    bb=float(b)
    lati=aa+bb/60
    (c,d)=divmod(float(loni),100)
    cc=int(c)
    dd=float(d)
    loni=cc+(dd/60)
    
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TIME_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I,emolt_sensor.SALT&emolt_sensor.SITE='
    dataset = get_dataset(url + '"' + site[k] + '"')
    var = dataset['emolt_sensor']
    print 'extracting eMOLT data using PyDap... hold on'
    depth = list(var.DEPTH_I)
    distinct_dep=unique(depth)
    sites.append(site[k])
    lat.append(lati)
    lon.append(loni)
    depthunique.append(distinct_dep)

sitetotal=[]
lattotal=[]
lontotal=[]
for i in range(len(depthunique)):
    for m in range(len(depthunique[i])):
        if abs(depthunique[i][m]-50)<10:
            print site[i],lat[i],lon[i],depthunique[i]
            sitetotal.append(site[i])
            lattotal.append(lat[i])
            lontotal.append(lon[i])
d={'site':sitetotal,'lat':lattotal,'lon':lontotal}
dfemolt=pd.DataFrame(d)
dfemolt = dfemolt.drop_duplicates(cols='site', take_last=True)
dfemolt['sequence']=range(len(dfemolt))
dfemolt.index=dfemolt.sequence
    

    
dfn=pd.read_csv('NERACOOS.csv',sep=',',index_col=0,names=['site','lat','lon','depth'])
for j in range(len(dfn)):
    index,distance=nearlonlat(dfemolt.lon,dfemolt.lat,dfn.lon.values[j],dfn.lat.values[j])
    print dfn.index[j],dfn.lon.values[j],dfn.lat.values[j],dfemolt.site[index],dfemolt.lon[index],dfemolt.lat[index],distance
    
