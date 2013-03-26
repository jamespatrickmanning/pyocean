# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:52:41 2013

@author: jmanning
"""
import netCDF4
import pandas as pd
from utilities import nearlonlat
def getFVCOM_bottom_tempsalt_netcdf(lati,loni,starttime,endtime,layer,vname):#vname='temp'or'salinity'
        '''
generate mod data as a DataFrame
according to time and local position
different from getFVCOM_bottom_temp:
this function only return time-temp dataframe and ues netcdf4
getFVCOM_bottom_temp return depth and temp
        '''
        urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
        nc = netCDF4.Dataset(urlfvcom)
        nc.variables
        lat = nc.variables['lat'][:]
        lon = nc.variables['lon'][:]
        times = nc.variables['time']
        jd = netCDF4.num2date(times[:],times.units)
        var = nc.variables[vname]
        print 'Now find the coincide timestample'
        inode = nearlonlat(lon,lat,loni,lati)
        print inode
        modindex=netCDF4.date2index([starttime,endtime],times,select='nearest')
        modtso=pd.DataFrame(var[modindex[0]:modindex[1],layer,inode],index=jd[modindex[0]:modindex[1]])
        return modtso