# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:42:41 2012

@author:huanxin
"""
import pytz 
from matplotlib.dates import num2date,date2num
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy as np
import datetime as dt

from hx import getcodar_ctl_file,plot_getsst
from getdata import getdrift
from basemap import basemap_standard
drifter='pro' #"processed" or "raw"
option='3' # what is "option 1"?

def range_latlon(filename,driftnumber): # function neede in case of "raw" drifter date
  d=ml.load(filename)
  id=ml.find(d[:,0]==int(driftnumber))
  lat1=d[id,8]
  lon1=d[id,7]
  maxlon=max(lon1)
  minlon=min(lon1)
  maxlat=max(lat1)
  minlat=min(lat1)
  return maxlon,minlon,maxlat,minlat,lat1,lon1

utc = pytz.timezone('UTC')
png_num=0 #for save picture
#option=raw_input("If you have a file of column lat and lon,please input '1'\nIf you want to input points' location, please input '2'\n"
#"If you want to use the control file,please input '3'\n")
if option=='1':
    datetime_wanted=date2num(dt.datetime.strptime(raw_input("please input datetime you wanted, the format like: 2012,8,26,0,0\n"),'%Y,%m,%d,%H,%M'))
    filename=raw_input('Please input your file path and name:\n')
    maxlon,minlon,maxlat,minlat,lat,lon=range_latlon(filename)

if option=='2':
    datetime_wanted=date2num(dt.datetime.strptime(raw_input("please input datetime you wanted, the format like: 2012,8,26,0,0\n"),'%Y,%m,%d,%H,%M'))
    lat_list=raw_input("Please input points SW & NE latitude in order,and split them by ',':")
    lon_list=raw_input("Please input points lon in order,and split them by ',':")
    lat1=lat_list[0:].split(',')
    lon1=lon_list[0:].split(',')
    lat,lon=[],[]
    for q in range(len(lon1)):
        lat.append(float(lat1[q]))
        lon.append(float(lon1[q]))
    maxlon=max(lon1)
    minlon=min(lon1)
    maxlat=max(lat1)
    minlat=min(lat1)  

if option=='3':
    inputfilename='getcodar_bydrifter_ctl.txt' #default control file
    (datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size)=getcodar_ctl_file(inputfilename)
    if drifter=='raw':
       maxlon,minlon,maxlat,minlat,lat,lon=range_latlon(filename,driftnumber)
    else:
       [lat, lon, datet, dep, time0, yearday]=getdrift(driftnumber) #uses pydap to get remote drifter data
       maxlon=max(lon)
       minlon=min(lon)
       maxlat=max(lat)
       minlat=min(lat)    


#make sure the picture can show lat and lon clearly
if maxlat-minlat<=0.1:
        maxlat=maxlat+0.01
        minlat=minlat-0.01
if maxlon-minlon<=0.1:
        maxlon=maxlon+0.01
        minlon=minlon-0.01

gbox=[minlon-1.0,maxlon+1.0, minlat-0.03, maxlat+0.03] # get edge for get sst
for x in range(num):
     
  ask_input=num2date(datetime_wanted) #get time for getsst
  #plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')
  plot_getsst(ask_input,utc,gbox)
  lat_wanted=lat[-1]
  lon_wanted=lon[-1]
    #find wanted point lat,lon

  #plt.plot(lon_wanted,lat_wanted,'.',markersize=30,color='m',label='end')
  plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),linewidth=3,color='black')
  #plt.plot(lon[0],lat[0],'.',markersize=20,color='g',label='start')  # start time
  plt.annotate('start',xy=(lon[0],lat[0]),xytext=(lon[0]+(maxlon-minlon)/10,lat[0]+(maxlat-minlat)/10),color='white',arrowprops=dict(facecolor='white',frac=0.3, shrink=0.05))
  plt.annotate('end',xy=(lon[-1],lat[-1]),xytext=(lon[-1]+(maxlon-minlon)/10,lat[-1]-(maxlat-minlat)/5),color='white',arrowprops=dict(facecolor='white',frac=0.3, shrink=0.05))
  plt.title('Drifter '+driftnumber+' and '+ask_input.strftime('%d %b %Y')+' SST')
basemap_standard([int(minlat),np.ceil(maxlat)],[int(minlon-1.5),np.ceil(maxlon)+1.0],2.0) #overrides xlim and ylims set previously 
plt.show()