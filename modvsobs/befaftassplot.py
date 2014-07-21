# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:33:49 2013

@author: yacheng and jmanning

Compares time series before and after assimilation
for all months in 2008 and generates Figure 13a and 13b

Note: I ran it in Dec 2013 and found it took some time ~hour
Note: I modified it in June 2014 to be compatible with ERDDAP extraction of eMOLT data

Loops through one month at a time since that is how the "before assimilation" files are available.

"""
from pydap.client import open_url
from matplotlib.dates import num2date
import matplotlib.pyplot as plt
import pandas as pd
from numpy import float64
from datetime import datetime, timedelta
import datetime as dt
import numpy as np
import sys
import netCDF4
from pylab import unique
import pytz
sys.path.append('../modules')
from getdata import getemolt_latlon,getobs_tempsalt
from conversions import dm2dd,f2c

###############################
#  HARDCODES
site=['NL01']
#site=['TA14']
aorb='a'
layer=44
intend_to='temp'##############notice intend_to can be 'temp'or'salinity'
vname=intend_to
surf_or_bott='bott'
month=range(1,13)
#month=[1,2,3,4,5,6,8,9,10,11,12]
outputplotdir='/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/'
color1='black'
color2='black'
color3='black'
############################

def nearlonlat(lon,lat,lonp,latp):
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    # dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    #min_dist=np.sqrt(dist2[i])
    return i#,min_dist

# loop through each site and then each month
for k in range(len(site)):
    fig=plt.figure(figsize=(15,10))
    ax=fig.add_subplot(111)
    for m in range(len(month)):
        month_time=month[m]
        #################read-in obs data##################################
        print site[k]
        [lati,loni,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        if surf_or_bott=='bott':
            dept=[bd-0.25*bd,bd+.25*bd]
        else:
            dept=[0,5]
        ######################################################################################
        if month_time<12:
           input_time=[dt.datetime(2008,int(month_time),1,0,0,0,0,pytz.UTC),dt.datetime(2008,int(month_time)+1,1,0,0,0,0,pytz.UTC)]
        else:
           input_time=[dt.datetime(2008,int(month_time),1,0,0,0,0,pytz.UTC),dt.datetime(2008,int(month_time),31,0,0,0,0,pytz.UTC)]
        dep=dept

        print 'extracting eMOLT data using ERDDAP.. hold on'      
        (datet,temp,depths)=getobs_tempsalt(site[k],input_time)
        obstso=pd.DataFrame(temp,index=datet)
        print 'obs Dataframe is ready .. now getting model before assimilation'
        if month_time<10:
            month_time=str(0)+str(month_time)
            urlbeforeassi='http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT/gom'+str(month_time)+'_0001.nc'
            nb = netCDF4.Dataset(urlbeforeassi)
            nb.variables
            latb = nb.variables['lat'][:]
            lonb = nb.variables['lon'][:]
            timesb = nb.variables['time']
            jdb = netCDF4.num2date(timesb[:],timesb.units)
            for kk in range(len(jdb)): # make these model times timezone aware
               jdb[kk]=jdb[kk].replace(tzinfo=pytz.UTC)
            varb = nb.variables[vname]
            print 'Now find the index of space and time in the before assimilation model'
            inodeb = nearlonlat(lonb,latb,loni,lati)
            #print inodeb
            beftso=pd.DataFrame(varb[:,layer,inodeb],index=jdb)
            ###http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT_temp/gom3_200801.nc
            urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT_temp/gom3_2008'+str(month_time)+'.nc'
            nc = netCDF4.Dataset(urlfvcom)
            nc.variables
            lat = nc.variables['lat'][:]
            lon = nc.variables['lon'][:]
            times = nc.variables['time']
            jd = netCDF4.num2date(times[:],times.units)
            for kk in range(len(jd)): # make these model times timezone aware
               jd[kk]=jd[kk].replace(tzinfo=pytz.UTC)
            var = nc.variables['temp']
            print 'Now find the index of space and time in the AFTER assimilation model'
            inode = nearlonlat(lon,lat,loni,lati)
            #print inode
            modtso=pd.DataFrame(var[:,layer,inode],index=jd)
            ####before assimulate#######
        
            badindex=[]
            for ii in range(len(modtso)):
                tdelta=[]
                for j in range(len(obstso)):
                    tdelta.append(abs(modtso.index[ii] - obstso.index[j]))
                if min(tdelta)>timedelta(hours=0.5):
                       #print min(tdelta),ii
                       badindex.append(ii)
                       #print ii
            modtso=modtso.drop(modtso.index[badindex])
            beftso=beftso.drop(beftso.index[badindex])

            #rmsa=np.sqrt((sum((obstso.values-modtso.values)**2))/len(obstso))
            #rmsb=np.sqrt(sum((obstso.values-beftso.values)**2)/len(obstso))
            #print "rmsa"+str(rmsa),"rmsb"+str(rmsb)
     
        
            ax.plot(obstso.index,obstso[0].values,'-',color=color1)
            ax.plot(modtso.index,modtso[0].values,'--',color=color2)
            ax.plot(beftso.index,beftso[0].values,':',color=color3)
        print 'WARNING: '+str(len(badindex))+' points removed since there was not a matching observation time'        
    ax.set_ylabel('Temperature',fontsize=20)
    ax.set_title('Bottom temperature at '+str(site[k]),fontsize=18)
    ax.grid(True)
    plt.legend(['observed','after assimulation','before assimulation'],loc='upper right',# bbox_to_anchor=(1.01, 1.20),
                  ncol=10, fancybox=True, shadow=True,prop={'size':20})
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.show()
    plt.savefig(outputplotdir+'fig13'+aorb+'_'+str(site[k])+'_bottTEMPERATUREassimulation.png')
    plt.savefig(outputplotdir+'fig13'+aorb+'_'+str(site[k])+'_bottTEMPERATUREassimulation.eps')
        
