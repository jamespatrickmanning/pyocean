# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:33:49 2013

Calculates the change in modeled bottom temperature due to assimilation as a function of distance away from the site.
Loops through multple fractions of a degree and looks in four directions (E,W,N,S) and then calculates a RMS

@author: yacheng and jmanning
"""
from pydap.client import open_url
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
import numpy as np
import sys
sys.path.append('../modules')
from getdata import getemolt_latlon
from conversions import dm2dd
import netCDF4

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
    return i#,min_dist 

#site=['JS06']#,'BS02','BD01','AG01','BF01','NL01','SJ01','TA14']
site=['RB02']
layer=44
intend_to='temp'##############notice intend_to can be 'temp'or'salinity'
vname=intend_to
surf_or_bott='bott'
degree=[0.0,0.025,0.05]#,0.3]
ddir='/net/data5/jmanning/modvsobs/'
month=range(1,12)
f = open(ddir+'distance_affect.csv', 'w')
for k in range(len(site)):
   print site[k]   
   fig=plt.figure()
   #[lati,loni,on,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
   #[lati,loni]=dm2dd([lati],[loni])#converts decimal-minutes to decimal degrees
   lati=[41.0]
   loni=[-67.0]
   for d in range(len(degree)): #loop through different distances away from the site
     moddatadf= pd.DataFrame()  #initialize "after" assimilation dataframe
     befdatadf= pd.DataFrame()  #initialize "before" assimilation dataframe
     print "now degree is "+str(degree[d])
     print "case, month, site, degree_offset, long, lat"
     lati=[lati[0]+degree[d],lati[0]-degree[d]]
     loni=[loni[0]+degree[d],loni[0]-degree[d]]   
     for m in range(len(month)): # unfortunately, we have monthly files in this case
             month_time=month[m]   
#################read-in obs data##################################
             if month_time<12:
               input_time=[dt(2008,int(month_time),1),dt(2008,int(month_time)+1,1)]
             else:
               input_time=[dt(2008,int(month_time),1),dt(2008,int(month_time),31)]             
             if month_time<10:
                   month_time=str(0)+str(month_time)            
             urlbeforeassi='http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT/gom'+str(month_time)+'_0001.nc'            
             nb = netCDF4.Dataset(urlbeforeassi)
             nb.variables
             latb = nb.variables['lat'][:]
             lonb = nb.variables['lon'][:]
             timesb = nb.variables['time']
             jdb = netCDF4.num2date(timesb[:],timesb.units)
             varb = nb.variables[vname]
             if d==0:
                 ind=[0] #in first case we are looking at distance =0
             else:
                 ind=range(len(lati))
             for aa in ind:
               for oo in ind:
                 print 'before: ',month_time,site[k],str(degree[d]),str(loni[oo]),str(lati[aa])
                 inodeb = nearlonlat(lonb,latb,loni[oo],lati[aa])
                 beftso=pd.DataFrame(varb[:,layer,inodeb],index=jdb)
                 befdatadf=befdatadf.append(beftso)
             #print "beftso is done"
             urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/eMOLT_temp/gom3_2008'+str(month_time)+'.nc'
             nc = netCDF4.Dataset(urlfvcom)
             nc.variables
             lat = nc.variables['lat'][:]
             lon = nc.variables['lon'][:]
             times = nc.variables['time']
             jd = netCDF4.num2date(times[:],times.units)
             var = nc.variables['temp']
             for aa in ind:
               for oo in ind:
                 print ' after: ',month_time,site[k],str(degree[d]),str(loni[oo]),str(lati[aa])
                 inode = nearlonlat(lon,lat,loni[oo],lati[aa])
                 modtso=pd.DataFrame(var[:,layer,inode],index=jd)   
                 moddatadf=moddatadf.append(modtso)
             #print "modtso is done"
             #print str(month_time)+" has done"
     diff=pd.DataFrame(index=moddatadf.index,data=befdatadf.values-moddatadf.values)
     meandiff=np.mean(abs(diff.values)) 
     plt.plot([degree[d]]*len(diff.values),diff.values,'*',markersize=10)
     plt.plot(degree[d],meandiff,'o',markersize=30)      
     rmsob=np.sqrt((sum((diff.values)**2))/len(diff))
     print "site, distance, meandiff, rms"
     print site[k]+','+str(degree[d])+','+str(meandiff)+','+str(rmsob[0])
     f.write(site[k]+','+str(degree[d])+','+'%10.2f' % meandiff+','+ '%10.2f' % rmsob[0]+'\n')
     del befdatadf,moddatadf
     print 'get next distance'
   plt.grid()
   plt.ylabel('model(before)-model(after) (degC)')
   plt.xlabel('distance')
   plt.title(site[k]+' assimilation influence change with distance')
   plt.show()     
f.close()