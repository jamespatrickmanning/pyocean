
# -*- coding: utf-8 -*-
"""
Created on Thu May 02 08:27:24 2013

@author: Huanxin
"""
####################################################
#get wind data from neracoos OpenDap,generate a df which includ time,lat,lon.current speed,current direction,depth.
####################################################
from matplotlib.dates import date2num, num2date
import datetime as dt

import sys
import matplotlib.pyplot as plt
import numpy as np
from pandas import *
pydir='../'

sys.path.append(pydir)

from neracoos_def import get_neracoos_ctl,get_id_s_id_e_id_max_url,get_neracoos_wind_data

'''
Dataset: A01.sbe37.historical.50m.nc
lat, 42.5180647466176
lon, -70.5652227043109
Dataset: B01.sbe37.historical.20m.nc
lat, 43.1806472713891
lon, -70.4276963702579
Dataset: D02.sbe37.historical.10m.nc
lat, 43.7617166666667
lon, -69.9878833333333
Dataset: E01.sbe37.historical.50m.nc
lat, 43.7151721464189
lon, -69.3557710445127
Dataset: E02.sbe37.historical.50m.nc
lat, 43.7065
lon, -69.32
Dataset: F01.sbe37.historical.50m.nc
lat, 44.0556001811715
lon, -68.9967173062176
Dataset: F02.sbe37.realtime.1m.nc
lat, 44.3878
lon, -68.8308
Dataset: I01.sbe37.historical.50m.nc
lat, 44.1059919278702
lon, -68.1084972935196
Dataset: M01.sbe37.historical.250m.nc
lat, 43.4897
lon, -67.8815
Dataset: N01.sbe37.historical.180m.nc
lat, 42.3314893622147
lon, -65.9064274838096
'''

 
inputfilename='./get_neracoos_ctl.txt'
mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites=get_neracoos_ctl(inputfilename) #get input from input file
model='met'
sdtime_n=date2num(mindtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of start time
edtime_n=date2num(maxdtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of end time
for index_site in range(len(sites)):
    url='http://neracoos.org:8080/opendap/'+sites[index_site]+'/'+sites[index_site]+'.'+model+'.historical.nc?' 
    
    id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n) # 'maxtime',the max time in this url, "id_s",the index of start time we want
    if mintime=='':   
        histvsreal='1' #"histvsreal" can help us judge if this  site has historical data.
        url='http://neracoos.org:8080/opendap/'+sites[index_site]+'/'+sites[index_site]+'.'+model+'.realtime.nc?'     
        id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n) # 'maxtime',the max time in this url, "id_s",the index of start time we want
        print 'realtime from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))
    else:
        print 'historical from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))
        histvsreal=''
    if id_e0<>'':  
      (period_str,wind_all)=get_neracoos_wind_data(url,id_s,id_e0,id_max_url) #get data from web neracoos
      df = DataFrame(np.array(wind_all),index=period_str,columns=['depth','wind','direction'])
    else:
        print "According to your input, there is no data here"    
    if histvsreal<>'1':
      if   maxtime<edtime_n: #make sure if we need a realtime data
        url='http://neracoos.org:8080/opendap/'+sites[index_site]+'/'+sites[index_site]+'.'+model+'.realtime.nc?'     
        id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
        print 'realtime from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))
        if id_e<>'':     
           (period_str,wind_all)=get_neracoos_wind_data(url,id_s,id_e,id_max_url)  #get data from web neracoos
           if id_e0=='':
              df = DataFrame(np.array(wind_all),index=period_str,columns=['depth','wind','direction'])
           else:              
              df = df.append(DataFrame(np.array(wind_all),index=period_str,columns=['depth','wind','direction']))#combine them in DataFrame  
    df.plot()
    plt.show()
    df.to_csv('wind_'+sites[index_site]+'.csv') #save it to a csv file





























'''
mindtime1,maxdtime1,i_mindepth,i_maxdepth,site2,mindtime,maxdtime
	  #According to the conditions to select data from "emolt_sensor"
url2="http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.TIME_LOCAL,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I&emolt_sensor.TIME_LOCAL>="+str(mindtime1)+"&emolt_sensor.TIME_LOCAL<="\
+str(maxdtime1)+"&emolt_sensor.DEPTH_I>="+str(i_mindepth)+"&emolt_sensor.DEPTH_I<="+str(i_maxdepth)+site2
try:   
    dataset1=open_url(url2)
except:
    print 'Sorry, '+url2+' not available' 
    sys.exit(0)
emolt_sensor=dataset1['emolt_sensor']
try:   
	          sites2=list(emolt_sensor['SITE'])
except:
	          print "'Sorry, According to your input, here are no value. please check it! ' "
	          sys.exit(0) 
	  #sites2=list(emolt_sensor['SITE'])
time=list(emolt_sensor['TIME_LOCAL'])
yrday0=list(emolt_sensor['YRDAY0_LOCAL'])
temp=list(emolt_sensor['TEMP'])
depth1=list(emolt_sensor['DEPTH_I'])
	

	  time1,wind,yrday01,sites1,depth=[],[],[],[],[]
	  for m in range(len(time)):
	      #if mindtime<=dt.datetime.strptime(str(time[m]),'%Y-%m-%d')<=maxdtime:
	      if date2num(mindtime)<=yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))<=date2num(maxdtime):
	      #if str(time[m])=='2012-01-01':
	        wind.append(temp[m])
	        yrday01.append(yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d')))
	        sites1.append(sites2[m])
	        time1.append(date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))) 
	        depth.append(depth1[m])
	  #print len(wind)     
	  return time1,yrday01,wind,sites1,depth,'''

