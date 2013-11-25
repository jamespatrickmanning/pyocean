# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:32:36 2012

@author: huanxin

This use for plot track of drifter, use ctl file "getcodar_ctl.txt"

JManning modifications:
    It apparently uses "raw" drifter data rather then the webserved ORACLE data.
    
"""
from matplotlib.dates import date2num, num2date
import datetime
import pylab
import sys
import numpy as np
import matplotlib.pyplot as plt
pydir='../'
sys.path.append(pydir)
from hx import getcodar_ctl_file,getdrift_raw_range_latlon,getdrift_raw

###############################################
inputfilename='./getcodar_bydrifter_ctl.txt'
(datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size)=getcodar_ctl_file(inputfilename)
id3=int(driftnumber)  #change format

(maxlon,minlon,maxlat,minlat)=getdrift_raw_range_latlon(filename,id3,interval,datetime_wanted,num,step_size)
for i in range(5):
    if maxlat-minlat<=0.1:
        maxlat=maxlat+0.01
        minlat=minlat-0.01
    if maxlon-minlon<=0.1:
        maxlon=maxlon+0.01
        minlon=minlon-0.01
gbox=[minlon-0.03,maxlon+0.03, minlat-0.03, maxlat+0.03]
# get the edge of the picture 

for x in range(num): 
  (lat,lon,time1)=getdrift_raw(filename,id3,interval,datetime_wanted)   
  fig = plt.figure()
  ax = fig.add_subplot(111)   
  plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')
  lat_wanted=lat[-1]
  lon_wanted=lon[-1]
  plt.plot(lon_wanted,lat_wanted,'.',markersize=30,color='r',label='end')
  
    #plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)))
  plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color='black')
    
    #basemap_usgs([minlat-1,maxlat+1],[minlon-1,maxlon+1],'True')
  plt.plot(lon[0],lat[0],'.',markersize=20,color='g',label='start')  # start time
  pylab.ylim([minlat-0.02,maxlat+0.02])
  pylab.xlim([minlon-0.02,maxlon+0.02])
  ax.patch.set_facecolor('lightblue')

  plt.legend( numpoints=1,loc=2)  
  plt.savefig('./'+str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h' + '.png')
 
  datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))
  plt.close()


plt.close()