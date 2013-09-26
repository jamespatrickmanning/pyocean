# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:48:21 2013

@author: jmanning
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:33:49 2013

@author: jmanning
"""
from pydap.client import open_url
from matplotlib.dates import num2date
import matplotlib.pyplot as plt
from getdata import getemolt_latlon,getobs_tempsalt
from conversions import dm2dd,f2c
#from utilities import my_x_axis_format
import pandas as pd
from numpy import float64
from datetime import datetime, timedelta
#from models import getFVCOM_bottom_tempsalt_netcdf
import datetime as dt
import numpy as np
import sys
import netCDF4
from pylab import unique
def get_dataset(url):
    try:
        dataset = open_url(url)
    except:
        print 'Sorry, ' + url + 'is not available'
        sys.exit(0)
    return dataset
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
site=['NL01']
layer=44
intend_to='temp'##############notice intend_to can be 'temp'or'salinity'
vname=intend_to
surf_or_bott='bott'
month=range(1,13)
for k in range(len(site)):
    fig=plt.figure(figsize=(15,10))
    ax=fig.add_subplot(111)
    for m in range(len(month)):
        month_time=month[m]
#################read-in obs data##################################
        print site[k]
        [lati,loni,on,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        print bd
        [lati,loni]=dm2dd(lati,loni)#converts decimal-minutes to decimal degrees
        print lati,loni
        '''
[obs_dt,obs_temp]=getemolt_temp(site[k]) # extracts time series
obs_dtindex=[]
for kk in range(len(obs_temp)):
obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius
obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:10],'%Y-%m-%d'))
'''
        if surf_or_bott=='bott':
            dept=[bd[0]-0.25*bd[0],bd[0]+.25*bd[0]]
            
        else:
            dept=[0,5]
# (obs_dt,obs_temp,obs_salt,distinct_dep)=getobs_tempsalt(site[k],
######################################################################################
        if month_time<12:
          input_time=[dt.datetime(2008,int(month_time),1),dt.datetime(2008,int(month_time)+1,1)]
        else:
          input_time=[dt.datetime(2008,int(month_time),1),dt.datetime(2008,int(month_time),31)]
        dep=dept
        
        if month_time==1:
          url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TIME_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I,emolt_sensor.SALT&emolt_sensor.SITE='
          dataset = get_dataset(url + '"' + site[k] + '"')
          var = dataset['emolt_sensor']
          print 'extracting eMOLT data using PyDap... hold on'
          temp = list(var.TEMP)
          depth = list(var.DEPTH_I)
          time0 = list(var.YRDAY0_LOCAL)
          year_month_day = list(var.TIME_LOCAL)
          salt=list(var.SALT)
  
          print 'Generating a datetime ... hold on'
          datet = []
          for i in np.arange(len(time0)):
            #datet.append(num2date(time0[i]+1.0).replace(year=time.strptime(year_month_day[i], '%Y-%m-%d').tm_year).replace(day=time.strptime(year_month_day[i], '%Y-%m-%d').tm_mday))
            datet.append(num2date(time0[i]+1.0).replace(year=dt.datetime.strptime(year_month_day[i], '%Y-%m-%d').year).replace(month=dt.datetime.strptime(year_month_day[i],'%Y-%m-%d').month).replace(day=dt.datetime.strptime(year_month_day[i],'%Y-%m-%d').day).replace(tzinfo=None))
          #get the index of sorted date_time
          print 'Sorting mooring data by time'
          index = range(len(datet))
          index.sort(lambda x, y:cmp(datet[x], datet[y]))
          # reorder the list of date_time,u,v
          datet = [datet[i] for i in index]
          temp = [temp[i] for i in index]
          depth = [depth[i] for i in index]
          salt=[salt[i] for i in index]

        print 'Delimiting mooring data according to user-specified time'
        part_t,part_time,part_salt,distinct_dep= [],[],[],[]
        start_time = input_time[0]
        end_time = input_time[1]
        print start_time, end_time
        for i in range(len(temp)):
            if (start_time <= datet[i] <= end_time) & (dep[0]<=depth[i]<= dep[1]):
                part_t.append(temp[i])
                part_time.append(datet[i])
                part_salt.append(salt[i])
            
        distinct_dep.append(unique(depth))
        obs_temp=part_t
        obs_dt=part_time
        obs_salt=part_salt

        obs_dtindex=[]
        if intend_to=='temp':
            for kk in range(len(obs_temp)):
                obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius
                obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:19],'%Y-%m-%d %H:%M:%S'))
            obstso=pd.DataFrame(obs_temp,index=obs_dtindex)
        else:
            for kk in range(len(obs_salt)):
                obs_dtindex.append(datetime.strptime(str(obs_dt[kk])[:19],'%Y-%m-%d %H:%M:%S'))
            obstso=pd.DataFrame(obs_salt,index=obs_dtindex)
        print 'obs Dataframe is ready'
        try:
            starttime=obs_dt[0].replace(tzinfo=None)
        #endtime=obs_dt[-1].replace(tzinfo=None)
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
            print 'Now find the coincide before assinulate timestample'
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
            var = nc.variables['temp']
            print 'Now find the coincide timestample'
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

            rmsa=np.sqrt((sum((obstso.values-modtso.values)**2))/len(obstso))
            rmsb=np.sqrt(sum((obstso.values-beftso.values)**2)/len(obstso))
            print "rmsa"+str(rmsa),"rmsb"+str(rmsb)
     
        
            ax.plot(obstso.index,obstso[0].values,color='red')
            ax.plot(modtso.index,modtso[0].values,color='blue')
            ax.plot(beftso.index,beftso[0].values,color='green')
        except:
            m=m+1
        #del temp,datet,depth,salt,index    
        print 'WARNING: '+str(len(badindex))+' points removed since there was not a matching observation time'        
    ax.set_ylabel('Temperature',fontsize=20)
    ax.set_title('Bottom temperature at '+str(site[k]),fontsize=18)
    ax.grid(True)
    plt.legend(['observed','after assimulation','before assimulation'],loc='upper right',# bbox_to_anchor=(1.01, 1.20),
                  ncol=10, fancybox=True, shadow=True,prop={'size':20})
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.show()
    plt.savefig(str(site[k])+'_bottTEMPERATUREassimulation.png')
        