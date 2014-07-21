# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:45:35 2013

@author: jmanning
"""
import netCDF4
from datetime import datetime as dt
import numpy as np
import pandas as pd

def nearlonlat(lon,lat,lonp,latp):
    """
    i,min_dist=nearlonlat(lon,lat,lonp,latp) change
    find the closest node in the array (lon,lat) to a point (lonp,latp)
    input:
        lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
        lonp,latp - point on a sphere
        output:
            i - index of the closest node
            min_dist - the distance to the closest node, degrees
            For coordinates on a plane use function nearxy
            
            Vitalii Sheremet, FATE Project
    """
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    # dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    #min_dist=np.sqrt(dist2[i])
    return i#,min_dist 
st=dt(2001,5,1,0,0,0)
et=dt(2010,12,31,0,0,0)
layer=44
urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
nc = netCDF4.Dataset(urlfvcom)
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
times = nc.variables['time']
jd = netCDF4.num2date(times[:],times.units)
var = nc.variables['temp']
inode = nearlonlat(lon,lat,-69.5,43.5)
print 'getting time index'
modindex=netCDF4.date2index([st,et],times,select='nearest')
print 'Generating timeseries'
ts=var[modindex[0]:modindex[1],layer,inode]
print 'Generating time index'
idn=jd[modindex[0]:modindex[1]]
print 'Generating a dataframe of model data requested'
modtso=pd.DataFrame(ts,index=idn)