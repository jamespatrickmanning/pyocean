# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:15:34 2013
@author: J Manning
modified "modvsobs.py" to extract bottom velocity instead of temp & salt
"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import float64
from datetime import datetime, timedelta
import datetime as dt
import pandas as pd
import sys
import netCDF4
import pytz
# import our local modules
sys.path.append('../modules')
from getdata import getemolt_latlon,getobs_tempsalt
from conversions import dm2dd,f2c
from utilities import my_x_axis_format

##########################################################################
# HARDCODES
#all sites are listed in /data5/jmanning/modvsobs/totalcalculate_41sites_list.dat and the following line
#site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
vname='vel'  ##############notice vname can be 'temp', 'salinity', or 'vel'
surf_or_bott='bott'
outputdir='/net/data5/jmanning/modvsobs/'
lat=[40.985417,40.72486,42.069643]
lon=[-68.706695,-68.782795,-66.38201]
bdepth=[67,64,84]
site=[210,216,287]
obs_dt=[dt.datetime(2009,4,2,23,4,0),dt.datetime(2010,4,2,15,33,0),dt.datetime(2011,4,24,16,2,0)]
################################################

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
    
def getFVCOM_bottom_tempsaltvel_netcdf(lati,loni,starttime,endtime,layer,vname):#vname='temp'or'salinity'
        '''
        Function written by Yacheng Wang
        generates model data as a DataFrame
        according to time and local position
        different from getFVCOM_bottom_temp:
        this function only return time-temp dataframe and ues netcdf4
        getFVCOM_bottom_temp return depth and temp
        '''
        urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
        nc = netCDF4.Dataset(urlfvcom)
        nc.variables
        times = nc.variables['time']
        jd = netCDF4.num2date(times[:],times.units)
        if vname=='vel':
            u = nc.variables['u']
            v = nc.variables['v']
            lat = nc.variables['latc'][:]
            lon = nc.variables['lonc'][:]
        else:
            var=nc.variables[vname]
            lat = nc.variables['lat'][:]
            lon = nc.variables['lon'][:]
        inode = nearlonlat(lon,lat,loni,lati)
        modindex=netCDF4.date2index([starttime.replace(tzinfo=None),endtime.replace(tzinfo=None)],times,select='nearest')
        print modindex
        #print [u[modindex[0]:modindex[1],layer,inode][0],v[modindex[0]:modindex[1],layer,inode][0]]
        if vname=='vel':
            modtso=pd.DataFrame(np.array([u[modindex[0]:modindex[1],layer,inode],v[modindex[0]:modindex[1],layer,inode]]).T,index=jd[modindex[0]:modindex[1]])
            #modtso=pd.DataFrame(np.array([u[modindex[0],layer,inode],v[modindex[0],layer,inode]]).T,index=jd[modindex[0]])
        else:
            modtso=pd.DataFrame(var[modindex[0]:modindex[1],layer,inode],index=jd[modindex[0]:modindex[1]])
        return modtso
modtso = pd.DataFrame()
for k in range(len(site)):
        print site[k]
        #[lati,loni,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        lati=lat[k]
        loni=lon[k]

        ###################read-in model data#################################
        starttime=obs_dt[k]
        endtime=obs_dt[k]+timedelta(hours=1)

        print starttime
        if surf_or_bott=='bott':
                 modtso1=getFVCOM_bottom_tempsaltvel_netcdf(lati,loni,starttime,endtime,layer=44,vname=vname)
        else:
                 modtso1=getFVCOM_bottom_tempsaltvel_netcdf(lati,loni,starttime,endtime,layer=0,vname=vname)  
        modtso=pd.concat([modtso,modtso1])
        print modtso
modtso.to_csv(outputdir+'threesites_'+surf_or_bott+vname+'_mod.csv',index=True,header=False,na_rep='NaN',float_format='%10.4f')
