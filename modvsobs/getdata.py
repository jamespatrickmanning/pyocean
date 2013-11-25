# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:04:47 2013

@author: jmanning
"""

import csv
import matplotlib
from datetime import datetime
from matplotlib.dates import date2num, num2date
import datetime as dt
import scipy
import pylab
import sys
import time
from pydap.client import open_url
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
from matplotlib.dates import  DateFormatter
import numpy as np
import math
from conversions import dist
import pytz
utc = pytz.timezone('UTC')
#from basemap import basemap_usgs

def emolt_plotting(yrday,depth,temp,time11,samesites0,ax,k,ave_temp0,rgbcolors):
    #"ax" you can do like fig = plt.figure() ; ax = fig.add_subplot(111)
    #"k" "samesites0" ,this function should be in "for" loop,  for k in range(len(samesites0)): 
    # except "k", all of them should be a list
    #ave_temp0 means every average temperature for every samesites
    #rgbcolors is a color box, we select colors from it for plot
    temp0,yrday0=[],[]
    if temp<>[]:       
      depth111s=min(depth)
      # sorted Temperature by date,time   
      a=zip(yrday,temp)
      b=sorted(a, key=lambda a: a[0])
      for e in range(len(temp)):
        yrday0.append(b[e][0])
        temp0.append(b[e][1])     
      plt.plot(yrday0,temp0,color=rgbcolors[k],label=samesites0[k]+'(s): -'+str(int(depth111s))+','+str(round(ave_temp0[k],1))+'F',lw = 3)         
    plt.ylabel('Temperature')
    plt.title('temp from '+num2date(min(time11)).strftime("%d-%b-%Y")+' to '+num2date(max(time11)).strftime("%d-%b-%Y"))
    plt.legend()

#choose suited unit in x axis
    if max(time11)-min(time11)<5:
       monthsFmt = DateFormatter('%m-%d\n %H'+'h')
    if 5<=max(time11)-min(time11)<366:
       monthsFmt = DateFormatter('%m-%d')
    if max(time11)-min(time11)>366:
       monthsFmt = DateFormatter('%Y-%m')    
    ax.xaxis.set_major_formatter(monthsFmt)

    #ax.set_xlabel(str(num2date(min(time11)).year)+"-"+str(num2date(max(time11)).year),fontsize=17)
    #limit x axis length
    ax.set_xlabel('Notation:(s) means near the surface of sea')
    plt.xlim([min(time11),max(time11)+(max(time11)-min(time11))/2]) 
    plt.savefig('/net/home3/ocn/jmanning/py/huanxin/work/hx/please rename .png')   
    plt.show()



def getcodar(url, datetime_wanted):
    """
    Routine to track particles very crudely though the codar fields
    by extracting data from their respective OPeNDAP/THREDDS archives via the pyDAP method
    Example input: 
    datetime_wanted = datetime.datetime(2007,10,2)                     
    url = "http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06"
    """
    print datetime_wanted                
    
    dtime = open_url(url + '?time')
    id = ml.find(np.array(dtime['time']) == date2num(datetime_wanted) - date2num(dt.datetime(2001, 1, 1, 0, 0)))
    
    dataset = open_url(url + '?u[' + str(int(id)) + '],v[' + str(int(id)) + '],lat,lon,time[' + str(int(id)) + ']')
    print url + '?u[' + str(int(id)) + '],v[' + str(int(id)) + '],lat,lon,time[' + str(int(id)) + ']'   
    
    lat_array = dataset['lat']
    lon_array = dataset['lon']
    u1 = dataset['u']
    v1 = dataset['v']
    print lat_array
    u, v = [], []
    
    lat_vel = [lat for lat in lat_array]
    lon_vel = [lon for lon in lon_array] 
    
    [lon_vel, lat_vel] = pylab.squeeze(list(np.meshgrid(lon_vel, lat_vel)))   
    
    u1 = pylab.squeeze(list(np.array(u1.u[id])))
    v1 = pylab.squeeze(list(np.array(v1.v[id])))

    for y in range(len(u1)): 
        u.append(u1[y] / 100)    # converting to m/s
        v.append(v1[y] / 100)
        
    return lat_vel, lon_vel, u, v



def getcodar1(url, starttime, endtime):
    """
    returns all the velocity fields
    """
    try:          
        dataset = open_url(url + '?time')
        print dataset
    except:
        print 'Sorry, ' + url + ' not available' 
        sys.exit(0)

    jdmat_1 = dt.datetime(dataset) #units: days since 2001-01-01 00:00:00
    
    print jdmat_1
    lat_array = dataset['lat']
    lon_array = dataset['lon']
    u1 = dataset['u']
    v1 = dataset['v']
    #change array to list: lat & lon
    jdmat_m, u, v = [], [], []
    
    lat_vel = [lat for lat in lat_array]
    lon_vel = [lon for lon in lon_array] 
    lon_vel = np.array(lon_vel)
    lat_vel = np.array(lat_vel)
    
    lon_vel = lon_vel.reshape(np.size(lon_vel))
    lat_vel = lat_vel.reshape(np.size(lat_vel))

    jdmat_2 = [j for j in jdmat_1] 
        
    id = list(np.where(jdmat_2 > np.array(jdmat_2[-1] - 20))[0])
    for i in id:
        u.append(u1[i] / 100)# converting to m/s
        v.append(v1[i] / 100)
        jdmat_m.append(jdmat_1[i])
    print jdmat_m[0], len(jdmat_m), len(u[0]), len(lat_vel), len(lon_vel)
    return jdmat_m, lat_vel, lon_vel, u, v


def getemolt_latlon(site):
    """
    get data from emolt_sensor 
    """
    urllatlon = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE,emolt_site.LAT_DDMM,emolt_site.LON_DDMM,emolt_site.ORIGINAL_NAME,emolt_site.BTM_DEPTH&emolt_site.SITE='
    dataset = open_url(urllatlon+'"'+site+'"')
    print dataset
    var = dataset['emolt_site']
    lat = list(var.LAT_DDMM)
    lon = list(var.LON_DDMM)
    original_name = list(var.ORIGINAL_NAME)
    bd=list(var.BTM_DEPTH)  
    return lat[0], lon[0], original_name,bd


def getcodar_ctl_file(inputfilename):
#open file and read,It is used for get model data
  f=open(inputfilename)  
  dtime=f.readline()
  dtime=dtime[0:dtime.index(']')].strip('[')
  datetime_wanted=date2num(dt.datetime.strptime(dtime,'%Y,%m,%d,%H,%M')) 
  
  filename=f.readline()
  filename=filename[0:filename.index(']')].strip('[').split(',')
  filename=filename[0]
  
  driftnumber=f.readline()
  driftnumber=driftnumber[0:driftnumber.index(']')].strip('[').split(',')
  driftnumber=driftnumber[0] 
  
  num_interval=f.readline()
  num_interval=num_interval[0:num_interval.index(']')].strip('[').split(',')
  print 'num of picture, interval time, step size :'+str(num_interval)
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=dt.timedelta( 0,interval*60*60 )
  step_size=int(num_interval[2])

  
  model_option=f.readline()
  model_option=model_option[0:model_option.index(']')].strip('[')
  model_option=model_option[0]
  
  if model_option=='1':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
  if model_option=='2':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
  if model_option=='3':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
  if model_option=='4':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
  if model_option=='5':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"
  return datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size

    

def getcodar_ctl_file_edge(inputfilename):
#open file and read,It is used for get model data,this can get edge from ctl file
  f=open(inputfilename)  
  dtime=f.readline()
  dtime=dtime[0:dtime.index(']')].strip('[')
  datetime_wanted=date2num(dt.datetime.strptime(dtime,'%Y,%m,%d,%H,%M')) 
  
  latlon=f.readline()
  latlon=latlon[0:latlon.index(']')].strip('[').split(',')
  lat_max=float(latlon[0])
  lat_min=float(latlon[1])
  lon_max=float(latlon[2])
  lon_min=float(latlon[3])
  
  
  num_interval=f.readline()
  num_interval=num_interval[0:num_interval.index(']')].strip('[').split(',')
  #print num_interval
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=dt.timedelta( 0,interval*60*60 )

  '''
  num_interval=f.readline()
  num_interval=num_interval[0:num_interval.index(']')].strip('[').split(',')
  print num_interval
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=datetime.timedelta( 0,interval*60*60 )
  step_size=int(num_interval[2])
  '''
  
  model_option=f.readline()
  model_option=model_option[0:model_option.index(']')].strip('[')
  model_option=model_option[0]
  
  if model_option=='1':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
  if model_option=='2':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
  if model_option=='3':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
  if model_option=='4':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
  if model_option=='5':
      url="http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"
  return datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime


def getcodar_ctl_id(model_option,url,datetime_wanted):
    if model_option=='1':
        dtime=open_url(url+'?time')
        dd=dtime['time']  
        print "This option has data from "+str(num2date(dd[0]+date2num(dt.datetime(2009, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(dt.datetime(2009, 1, 1, 0, 0))))
        id=datetime_wanted-date2num(dt.datetime(2009, 1, 1, 0, 0))
        id=str(int(id))
    else:
        dtime=open_url(url+'?time')
        dd=dtime['time']
        ddd=[]
        for i in list(dtime['time']):
            i=round(i,7)
            ddd.append(i)
        
        print "This option has data from "+str(num2date(dd[0]+date2num(dt.datetime(2001, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(dt.datetime(2001, 1, 1, 0, 0))))           
        id=ml.find(np.array(ddd)==round(datetime_wanted-date2num(dt.datetime(2001, 1, 1, 0, 0)),7))
        for i in id:
          id=str(i) 
        print 'codar id is  '+id
    return id    
#print id1
#id=date2num(datetime_wanted)-date2num(datetime.datetime(2009, 1, 1, 0, 0))

def getcodar_ctl_lalo(model_option,lat_max,lon_max,lat_min,lon_min):
    if model_option=='4':
        if lat_max>42.33:
            lat_max=42.33
        if lon_max>-66.78:
            lon_max=-66.78
        if lat_min<34.68:
            lat_min=34.68
        if lon_min<-75.84:
            lon_min=-75.84
        lat_max_i=str(int(11.11*(lat_max-34.68)))
        lat_min_i=str(int(11.11*(lat_min-34.68)))
        lon_max_i=str(int(8.5*(lon_max+75.84)))
        lon_min_i=str(int(8.5*(lon_min+75.84)))
        #lat_index='85'
        #lon_index='77'
    else:
        if lat_max>41.96:
            lat_max=41.96
        if lon_max>-68.03:
            lon_max=-68.03
        if lat_min<35.0:
            lat_min=35.0
        if lon_min<-75.99:
            lon_min=-75.99
        lat_max_i=str(int(18.534*(lat_max-35.0)))
        lat_min_i=str(int(18.534*(lat_min-35.0)))
        if int(lat_max_i)==int(lat_min_i):
            lat_max_i=str(int(lat_max_i)+1)
        lon_min_i=str(int(17.21*(lon_min+75.99)))
        lon_max_i=str(int(17.21*(lon_max+75.99)))
        if int(lon_max_i)==int(lon_min_i):
            lon_max_i=str(int(lon_max_i)+1)        
        #lat_index='129'
        #lon_index='137'
    print 'the index edge for codar is  '+lat_max_i,lat_min_i,lon_max_i,lon_min_i
    return lat_max_i,lon_max_i,lat_min_i,lon_min_i
  
  
def getcodar_edge(url,id,lat_max_i,lon_max_i,lat_min_i,lon_min_i):
  id=str(id)
  dataset=open_url(url+'?u['+id+':1:'+id+'][0:1:'+lat_max_i+'][0:1:'+lon_max_i+'],v['+id+':1:'+id+'][0:1:'+lat_max_i+'][0:1:'+lon_max_i+'],lat[0:1:'+lat_max_i+'],lon[0:1:'+lon_max_i+']')
   #print url+'?u['+str(int(id))+'],v['+str(int(id))+'],lat,lon,time['+str(int(id))+']'   
   #dataset=open_url(url)

  lat_array=dataset['lat']
  id=int(id)   
  lon_array=dataset['lon']
  u1=dataset['u']
  #print u1.u[id]
   #print np.size(lat_array)
   #print np.size(lon_array)
  
   
  v1=dataset['v']
#print list(u1.u[id])  
   #print np.size(v1)
   #jdmat_1=dataset['time']
   #jdmat_1=dataset['time']
   #change array to list: lat & lon
  lat_vel,lon_vel,jdmat_2,jdmat_m,u,v=[],[],[],[],[],[]
  for i in lat_array:
      lat_vel.append(i)
  for j in lon_array:
      lon_vel.append(j)
  #print lon_vel    
  [lon_vel,lat_vel]=pylab.squeeze(list(np.meshgrid(lon_vel,lat_vel)))   
  #print lat_vel[0],lat_vel[-1],lon_vel[0],lon_vel[-1]  
  u1=pylab.squeeze(list(np.array(u1.u[id])))
   #u1=np.array(u1.u.data)
  v1=pylab.squeeze(list(np.array(v1.v[id])))
   #print "size of v1 "+str(np.size(v1))
  #print list(u1)
  for y in range(len(u1)): 
      u.append(u1[y]/100)# converting to m/s
      v.append(v1[y]/100)
  #print u[0],u[-1]
  #print np.shape(u1)
  return lat_vel,lon_vel,u,v

def getdrift(id):
    """
    uses pydap to get remotely stored drifter data given an id number
    """
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/drift_data'
    
    dataset = get_dataset(url) 
     
    try:
        lat = list(dataset.drift_data[dataset.drift_data.ID == id].LAT_DD)
    except:
        print 'Sorry, ' + id + ' is not available'
        sys.exit(0)
        
    lon = list(dataset.drift_data[dataset.drift_data.ID == id].LON_DD)
    time0 = list(dataset.drift_data[dataset.drift_data.ID == id].TIME_GMT)
    yearday = list(dataset.drift_data[dataset.drift_data.ID == id].YRDAY0_GMT)
    dep = list(dataset.drift_data[dataset.drift_data.ID == id].DEPTH_I)
    datet = []
    # use time0('%Y-%m-%d) and yearday to calculate the datetime
    for i in range(len(yearday)):      
        datet.append(num2date(yearday[i]).replace(year=time.strptime(time0[i], '%Y-%m-%d').tm_year).replace(day=time.strptime(time0[i], '%Y-%m-%d').tm_mday))
    
    return lat, lon, datet, dep, time0, yearday




def getemolt_ctl(inputfilename):
   f=open(inputfilename)  
   select=f.readline()
   select=select[0:select.index(']')].strip('[').split(' ')
   select1=select[0]
   select2=select[1]
   select3=select[2]
   select4=select[3]
   select5=select[4]
   if select1 =='1':
       dtime=f.readline()
       dtime=dtime[0:dtime.index(']')].strip('[').split(';')
       mindtime=dt.datetime.strptime(dtime[0],'%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime(dtime[1],'%Y,%m,%d,%H,%M') 
   else:
       dtime=f.readline()
       
   if select2 =='1':
       idepth=f.readline()
       idepth=idepth[0:idepth.index(']')].strip('[').split(',')
       i_mindepth=float(idepth[0])
       i_maxdepth=float(idepth[1])
   else:
       i_mindepth=0
       i_maxdepth=2000
       dtime=f.readline()
       
   if select3 =='1':
       bdepth=f.readline()
       bdepth=bdepth[0:bdepth.index(']')].strip('[').split(',')
       b_mindepth=float(bdepth[0])
       b_maxdepth=float(bdepth[1])
   else:
       b_mindepth=0
       b_maxdepth=2000
       dtime=f.readline()
       
   if select4 =='1':
       latlon=f.readline()
       latlon=latlon[0:latlon.index(']')].strip('[').split(',')
       lat_max=float(latlon[0])
       lon_max=float(latlon[1])
       lat_min=float(latlon[2])
       lon_min=float(latlon[3])
   else:
       latlon=f.readline()
       lat_max=5000
       lon_max=5000  
       lat_min=3000
       lon_min=8000
       
   if select5 =='1':
       site=f.readline()
       site=site[0:site.index(']')].strip('[').split(',') 
   else:
       site=f.readline()
       site=''
       
   num=f.readline()
   num=int(num[0:num.index(']')].strip('['))
       
   return  mindtime,maxdtime,i_mindepth,i_maxdepth,b_mindepth,b_maxdepth,lat_max,\
lon_max,lat_min,lon_min,site,num


def getemolt_depth(b_mindepth,b_maxdepth,lat_max,lon_max,lat_min,lon_min,site1):
    #According to the conditions to select data from "emolt_sensor"
    url="http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE,emolt_site.BTM_DEPTH,emolt_site.LAT_DDMM,emolt_site.LON_DDMM&emolt_site.BTM_DEPTH<="+str(b_maxdepth)+"&emolt_site.BTM_DEPTH>="+str(b_mindepth)+"&emolt_site.LON_DDMM<="\
    +str(lon_max)+"&emolt_site.LON_DDMM>="+str(lon_min)+"&emolt_site.LAT_DDMM<="+str(lat_max)+"&emolt_site.LAT_DDMM>="+str(lat_min)+site1
    try:   
	           dataset=open_url(url)
    except:
	           print 'Sorry, '+url+' not available' 
	           sys.exit(0)
    emolt_site=dataset['emolt_site']
    try:   
	          sites=list(emolt_site['SITE'])
    except:
	          print "'Sorry, According to your input, here are no value. please check it! ' "
	          sys.exit(0)   
    sites=list(emolt_site['SITE'])
    depth_b=list(emolt_site['BTM_DEPTH'])
    

            
    lat_dd=list(emolt_site['LAT_DDMM'])
    lon_dd=list(emolt_site['LON_DDMM'])
    return sites,depth_b,lat_dd,lon_dd

'''
def getemolt_latlon(site,k):
    """
    get data from emolt_sensor 
    """
    urllatlon = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE,emolt_site.LAT_DDMM,emolt_site.LON_DDMM,emolt_site.ORIGINAL_NAME&emolt_site.SITE='
    dataset = open_url(urllatlon + site[k])
    var = dataset['emolt_site']
    lat = list(var.LAT_DDMM)
    lon = list(var.LON_DDMM)
    original_name = list(var.ORIGINAL_NAME)
    return lat[0], lon[0], original_name

def getemolt_latlon(site,k):
    """
    get data from emolt_sensor 
    """
    urllatlon = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE,emolt_site.LAT_DDMM,emolt_site.LON_DDMM,emolt_site.ORIGINAL_NAME&emolt_site.SITE="'+site[k]+'"'
    print urllatlon    
    dataset = open_url(urllatlon)
    var = dataset['emolt_site']
    lat = list(var.LAT_DDMM)
    lon = list(var.LON_DDMM)
    original_name = list(var.ORIGINAL_NAME)
    return lat[0], lon[0], original_name
'''
def getemolt_sensor(mindtime1,maxdtime1,i_mindepth,i_maxdepth,site2,mindtime,maxdtime):
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
	
	
	  time1,temp1,yrday01,sites1,depth=[],[],[],[],[]
	  for m in range(len(time)):
	      #if mindtime<=dt.datetime.strptime(str(time[m]),'%Y-%m-%d')<=maxdtime:
	      if date2num(mindtime)<=yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))<=date2num(maxdtime):
	      #if str(time[m])=='2012-01-01':
	        temp1.append(temp[m])
	        yrday01.append(yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d')))
	        sites1.append(sites2[m])
	        time1.append(date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))) 
	        depth.append(depth1[m])
	  #print len(temp1)     
	  return time1,yrday01,temp1,sites1,depth,


def getemolt_temp(site,k,input_time=[dt.datetime(1880,1,1),dt.datetime(2020,1,1)], dep=[0,1000]):
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TIME_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I&emolt_sensor.SITE='
    # get the emolt_sensor data
    dataset = get_dataset(url + '"' + site[k] + '"')
    var = dataset['emolt_sensor']
    print 'extracting eMOLT data using PyDap... hold on'
    temp = list(var.TEMP)
    depth = list(var.DEPTH_I)
    time0 = list(var.YRDAY0_LOCAL)
    year_month_day = list(var.TIME_LOCAL)  
    print 'Generating a datetime ... hold on'
    datet = []
#       for i in scipy.arange(len(time0)):
#            datet.append(num2date(time0[i]+1.0).replace(year=time.strptime(year_month_day[i], '%Y-%m-%d').tm_year).replace(day=time.strptime(year_month_day[i], '%Y-%m-%d').tm_mday))

        # Yacheng realized we do not really care about the hours-minutes-seconds so we can just use the days
    for i in scipy.arange(len(year_month_day)):
            datet.append(datetime.strptime(year_month_day[i],'%Y-%m-%d'))
    #get the index of sorted date_time
    print 'Sorting mooring data by time'
    index = range(len(datet))
    index.sort(lambda x, y:cmp(datet[x], datet[y]))
    #reorder the list of date_time,u,v
    datet = [datet[i] for i in index]
    temp = [temp[i] for i in index]
    depth = [depth[i] for i in index]
    print 'Delimiting mooring data according to user-specified time'  
    part_t,part_time,part_depth = [], [], []
    if len(input_time) == 2:
            start_time = input_time[0]
            end_time = input_time[1]
    if len(input_time) == 1:
            start_time = datet[0]
            end_time = start_time + input_time[0]
    print datet[0], datet[-1]
    for i in range(0, len(temp)):
            if (start_time <= datet[i] <= end_time) & (dep[0]<=depth[i]<= dep[1]):
                part_t.append(temp[i])
                part_time.append(datet[i])
                part_depth.append(depth[i])
    temp=part_t
    datet=part_time
    depth=part_depth
    return datet,temp,depth   


def getemolt_uv(site, input_time, dep):
    """
    get data from url, return datetime, u, v, depth
    input_time can either contain two values: start_time & end_time OR one value:interval_days
    """
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TIME_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I,emolt_sensor.U,emolt_sensor.V&emolt_sensor.SITE='
    # get the emolt_sensor data
    dataset = get_dataset(url + '"' + site + '"')
    var = dataset['emolt_sensor']
    print 'Making lists of mooring data'
    u = list(var.U)
    v = list(var.V)
    depth = list(var.DEPTH_I)
    time0 = list(var.YRDAY0_LOCAL)
    year_month_day = list(var.TIME_LOCAL)
  
    print 'Generating a datetime for mooring data'
    date_time, date_time_time = [], []
    for i in scipy.arange(len(time0)):
        date_time_time.append(num2date(time0[i]).replace(year=time.strptime(year_month_day[i], '%Y-%m-%d').tm_year).replace(day=time.strptime(year_month_day[i], '%Y-%m-%d').tm_mday))
        date_time.append(date2num(date_time_time[i]))#+float(4)/24) # makes it UTC
 
    #get the index of sorted date_time
    print 'Sorting mooring data by time'
    index = range(len(date_time))
    index.sort(lambda x, y:cmp(date_time[x], date_time[y]))
    #reorder the list of date_time,u,v
    date_time_num = [date_time[i] for i in index]
    u = [u[i] for i in index]
    v = [v[i] for i in index]
    depth = [depth[i] for i in index]

    print 'Delimiting mooring data according to user-specified time'  
    part_v, part_u, part_time = [], [], []
    if len(input_time) == 2:
        start_time = input_time[0]
        end_time = input_time[1]
    if len(input_time) == 1:
        start_time = date_time_num[0]
        end_time = start_time + input_time[0]
    print date_time_num[0], date_time_num[-1]
    for i in range(0, len(u)):
        if (start_time <= date_time_num[i] <= end_time) & (depth[i] == dep):
            part_v.append(v[i] / 100)
            part_u.append(u[i] / 100)
            part_time.append(num2date(date_time_num[i]))

    u = part_u
    v = part_v
    
    return part_time, u, v, depth, start_time, end_time


def getgomoos(site, *days):
    """
    Input: one value - interval days OR two values - start_time and end time
    """
    time_add_num = date2num(dt.datetime(1858, 11, 17))
    url = "http://neracoos.org:8080/opendap/" + site + "/" + site + ".aanderaa.realtime.nc"

    try:
        dataset = open_url(url)
    except Exception, e:
        print str(e)
        sys.exit(0)
    print url
    
    lat = dataset['lat']
    lon = dataset['lon']
    time0 = dataset['time']
    u = dataset['current_u']
    v = dataset['current_v']
    depth = dataset['depth']

    current_u = [i for i in u.current_u]
    current_v = [i for i in v.current_v]
    time_num = [(i + time_add_num) for i in time0]        
     
    if len(days) == 1:
        sdate = time_num[0]
        edate = sdate + days[0]
    sdate = time_num[0]
    if len(days) == 2:
        sdate = days[0]
        edate = days[1]

    part_v, part_u, part_time = [], [], []
    for i in range(0, len(current_u)):
        if sdate <= time_num[i] <= edate:
            part_v.append(current_v[i])
            part_u.append(current_u[i])
            part_time.append(time_num[i])
    if float(depth[0]) > 0:
        depth_i = -float(depth[0])
    else:
        depth_i = float(depth[0])

    if len(days) == 1:
        return  part_time, part_u, part_v, float(lat[0]), float(lon[0]), sdate, edate, depth_i
    if len(days) == 2:
        return  part_time, part_u, part_v, float(lat[0]), float(lon[0]), depth_i


def getsst(second):
    #get the index of second from the url
    time_tuple = time.gmtime(second)#calculate the year from the seconds
    year = time_tuple.tm_year
    if year < 1999 or year > 2010:
        print 'Sorry there might not be available data for this year'
    # WARNING: As of Jan 2012, this data is only stored for 1999-2010
    url1 = 'http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/' + str(year) + '?time[0:1:3269]'
    dataset1 = open_url(url1)
    times = list(dataset1['time'])
    # find the nearest image index
    index_second = int(round(np.interp(second, times, range(len(times)))))

    #get sst, time, lat, lon from the url
    url = 'http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/' + \
          str(year) + '?lat[0:1:1221],lon[0:1:1182],' + \
          'mcsst[' + str(index_second) + ':1:' + str(index_second) + \
          '][0:1:1221][0:1:1182]' + \
          ',time[' + str(index_second) + \
          ':1:' + str(index_second) + ']'
    try:
        dataset = open_url(url)
    except:
        print "Please check your url! Cannot access dataset."
        sys.exit(0)

    sst = dataset['mcsst'].mcsst
    time1 = dataset['time']
    lat = dataset['lat']
    lon = dataset['lon']
    return sst, time1, lat, lon



def gettrack_codar(lon_vel_list,lat_vel_list,u,v,startdate,hours,la,lo,uu,vv,q): # tracks particle at surface
            
            # calculate the points near la,la
            distance,index_lon,index_lat=nearxy(lon_vel_list,lat_vel_list,lo,la)
            
           
            #index_startdate=0#get the index of startdate
            # get u,v
            u1=float(u[index_lat][index_lon])
            v1=float(v[index_lat][index_lon])
            if u1<=-998.0/100:# case of no good data
                u1=uu[0]
                v1=vv[0]
                print "no good data in this lat lon at "+num2date(startdate+q+1).strftime("%d/%m/%y %H")+"h"
                
            #nsteps=scipy.floor(min(numdays,jdmat_m_num[-1])/daystep)
            # get the velocity data at this first time & place
            lat_k='lat'+str(1)
            lon_k='lon'+str(1)
            uu,vv,lon_k,lat_k,time=[],[],[],[],[]
            uu.append(u1)
            vv.append(v1)
            lat_k.append(la)
            lon_k.append(lo)
            time.append(startdate)
            
               
            # first, estimate the particle move to its new position using velocity of previous time steps
            lat1=lat_k[0]+float(vv[0]*3600)/1000/1.8535/60
            lon1=lon_k[0]+float(uu[0]*3600)/1000/1.8535/60*(scipy.cos(float(la)/180*np.pi))
                # find the closest model time for the new timestep
            '''
                jdmat_m_num_i=time[i-1]+float(1.0/24)
                time.append(jdmat_m_num_i)
                #print jdmat_m_num_i
                index_startdate=index_startdate+1

                #index_startdate=int(round(np.interp(jdmat_m_num_i,jdmat_m_num,range(len(jdmat_m_num)))))
                #find the point's index of near lat1,lon1
                index_location=nearxy(lon_vel,lat_vel,lon1,lat1)[1]
                ui=u[index_startdate][index_location]
                vi=v[index_startdate][index_location]
                #if u1<>-999.0/100:# case of good data
                vv.append(vi)
                uu.append(ui)
                
                # estimate the particle move from its new position using velocity of previous time steps
                lat_k.append(float(lat1+lat_k[i-1]+float(vv[i]*3600)/1000/1.8535/60)/2)
                lon_k.append(float(lon1+lon_k[i-1]+float(uu[i]*3600)/1000/1.8535/60*scipy.cos(float(lat_k[i])/180*np.pi))/2)
                #else:
                '''
                
                #  vv.append(0)
                #  uu.append(0)
                  # estimate the particle move from its new position using velocity of previous time steps
                #  lat_k.append(float(lat1))
                #  lon_k.append(float(lon1))      
            return lat1,lon1,time,uu,vv


def get_dataset(url):
    try:
        dataset = open_url(url)
    except:
        print 'Sorry, ' + url + 'is not available' 
        sys.exit(0)
    return dataset


##### what's the pormat of the data? #####
def get_w_depth(xi, yi, url='http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v03'):
    try:    
        dataset = open_url(url)
        
    except:
        print 'Sorry, ' + url + ' is not available' 
        sys.exit(0)

    #read lat, lon,topo from url
    xgom_array = dataset['lon']
    ygom_array = dataset['lat']
    dgom_array = dataset['topo'].topo

    #print dgom_array.shape, xgom_array[5:9],dgom_array[5]

    #convert the array to a list
    xgom, ygom = [], []
    
    for i in xgom_array:
        if i > xi[0] - 0.000834 and i < xi[0] + 0.000834:
            xgom.append(i)
  
    for i  in ygom_array:
        if i > yi[0] - 0.000834 and i < yi[0] + 0.000834:
            ygom.append(i)


    x_index, y_index = [], []
    (ys, xs) = dgom_array.shape##### what's this mean? #####

    for i in range(0, len(xgom)):
        x_index.append(int(round(np.interp(xgom[i], xgom_array, range(xs)))))
    for i in range(0, len(ygom)):
        y_index.append(int(round(np.interp(ygom[i], ygom_array, range(ys)))))
    
    dep, distkm, dist1 = [], [], []

    for k in range(len(x_index)):#### get a surface of lat and lon ######
        for j in range(len(y_index)):
            dep.append(dgom_array[(y_index[j], x_index[k])])
            distkm, b = dist(ygom[j], xgom[k], yi[0], xi[0],)##### what's this mean? #####
            dist1.append(distkm)

    #get the nearest,second nearest,third nearest point.
    dist_f_nearest = sorted(dist1)[0]
    dist_s_nearest = sorted(dist1)[1]
    dist_t_nearest = sorted(dist1)[2]
    
    index_dist_nearest = range(len(dist1))
    index_dist_nearest.sort(lambda x, y:cmp(dist1[x], dist1[y]))
    
    dep_f_nearest = dep[index_dist_nearest[0]]
    dep_s_nearest = dep[index_dist_nearest[1]]
    dep_t_nearest = dep[index_dist_nearest[2]]

    #compute the finally depth
    d1 = dist_f_nearest
    d2 = dist_s_nearest
    d3 = dist_t_nearest
    def1 = dep_f_nearest
    def2 = dep_s_nearest
    def3 = dep_t_nearest
    depth_finally = def1 * d2 * d3 / (d1 * d2 + d2 * d3 + d1 * d3) + def2 * d1 * d3 / (d1 * d2 + d2 * d3 + d1 * d3) + def3 * d2 * d1 / (d1 * d2 + d2 * d3 + d1 * d3)

    return depth_finally



def nearxy(x,y,x0,y0):
    distance=[]
    for i in range(0,np.size(x)):
      for l in range(0,len(y)):
         distance.append(abs(math.sqrt((x[i]-x0)**2+(y[l]-y0)**2)))
    min_dis=min(distance)
    #len_dis=len(distance)
    for p in range(0,len(x)):
      for q in range(0,len(y)):
          if abs(math.sqrt((x[p]-x0)**2+(y[q]-y0)**2))==min_dis:
              index_x=p
              index_y=q
    return min(distance),index_x,index_y


def plot_getsst(ask_input, utc, gbox):
    """
    Input:
    ask_input - day you want(format: 2009-08-01 18:34:00)
    utc - 'utc'
    gbox format: [-71, -70.5, 41.25, 41.75]
    """
    
    ask_datetime = dt.datetime.strptime(ask_input, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
    timtzone_ask_datetime = ask_datetime.astimezone(utc)
    second = time.mktime(timtzone_ask_datetime.timetuple())
    #year= dt.datetime.strptime(ask_input, '%Y-%m-%d %H:%M:%S').year

    sst, time1, lat, lon = getsst(second)

    # find the index for the gbox
    index_lon1 = int(round(np.interp(gbox[0], list(lon), range(len(list(lon))))))
    index_lon2 = int(round(np.interp(gbox[1], list(lon), range(len(list(lon))))))
    index_lat1 = int(round(np.interp(gbox[2], list(lat), range(len(list(lat))))))
    index_lat2 = int(round(np.interp(gbox[3], list(lat), range(len(list(lat))))))

    # get part of the sst
    sst_part = sst[1839, index_lat1:index_lat2, index_lon1:index_lon2]##### what's this line means? #####
    sst_part[(sst_part == -999)] = np.NaN # if sst_part = -999, convert to NaN
    #sst_part[numpy.isnan(sst_part)]=0 # then change NaN to 0
    X, Y = np.meshgrid(lon[index_lon1:index_lon2], lat[index_lat1:index_lat2])##### x-means rows and Y-means column #####
    #plot
    plt.figure()
    # get the min,max of lat and lon
    minlat = min(lat[index_lat1:index_lat2])
    maxlat = max(lat[index_lat1:index_lat2])
    minlon = min(lon[index_lon1:index_lon2])
    maxlon = max(lon[index_lon1:index_lon2])

    # plot map
    basemap_usgs([minlat, maxlat], [minlon, maxlon], False)

    # plot temperature
    CS = plt.contourf(X, Y, sst_part)
    plt.colorbar(CS, format='%1.2g' + 'C')

    # convert the seconds to datetime
    time_tuple = time.gmtime(time1[0])
    plt.title("RU COOL NOAA-19 Sea Surface Temperature: " + 
              dt.datetime(time_tuple.tm_year,
                                time_tuple.tm_mon,
                                time_tuple.tm_mday,
                                time_tuple.tm_hour,
                                time_tuple.tm_min,
                                time_tuple.tm_sec).strftime('%B_%d,%Y %H%M') + " GMT")
    plt.show()




def read_old_mooring_asc(filename):
    """
    Read old mooring data
    Input: filename
    Example data file: "Y:/moor/nech/NEC312b.dat"
    Returns: date_time_number, u, v, y
    """
    try:
        dataReader = csv.reader(open(filename, 'rb'))
    except:
        print "Cannot open file."
        sys.exit(0)
    
    verts = [row for row in dataReader]
    
    del verts[-1], verts[0] #del the first line and last line
    u, v, year, y, hour = [], [], [], [], []
    for i in range(0, len(verts)):
        #convert "space delimiter" to comma
        year.append(verts[i][0].split()[1])
        hour.append(verts[i][0].split()[2])
        u.append(verts[i][0].split()[6])
        v.append(verts[i][0].split()[7])
        y.append(0)
    hour_time = []
    for hour_i in hour:
        hourtime = hour_i[0:2] + ":" + hour_i[2:]
        hour_time.append(hourtime)
    date_time_number = []
    for i in range(0, len(year)):
        datetime = dt.datetime.strptime(year[i] + " " + hour_time[i], '%Y-%m-%d %H:%M')
        date_time_number.append(date2num(datetime))
    u = [float(i) for i in u]
    v = [float(i) for i in v]
    return date_time_number, u, v, y
  
  


def samesites_data(sites1,sites2,temp1,lat_dd,lon_dd):
    samesites=list(set(sites2).intersection(set(sites1)))
    if samesites==[]:
      print "Can not find eligible data, please re-enter the conditions"
      sys.exit(0)
    #get average Temperature, sorted sites by average Temperature
    ave_temp,samesites0,ave_temp0=[],[],[]
    for r in range(len(samesites)):
      temp_a=[]
      for s in range(len(sites1)):
         if sites1[s]==samesites[r]:
            temp_a.append(temp1[s]) 
      temp_ave=np.mean(temp_a)##### temp_ave=[]? need? #####
      ave_temp.append(temp_ave)
    c=zip(samesites,ave_temp)
    d=sorted(c, key=lambda c: c[1])##### d means? #####
    for g in range(len(samesites)):
      samesites0.append(d[g][0])
      ave_temp0.append(d[g][1])
    lat,lon=[],[]
    for y in range(len(samesites0)):
      for z in range(len(sites2)):
          if sites2[z]==samesites0[y]:
              lat.append(lat_dd[z])
              lon.append(lon_dd[z])  
    samesites=samesites0
    ave_temp=ave_temp0
    return samesites,ave_temp,lat,lon

def getobs_tempsalt(site,input_time,dep):
    """
    get data from url, return datetime, temperature, and start and end times
    input_time can either contain two values: start_time & end_time OR one value:interval_days
    """
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TIME_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I,emolt_sensor.SALT&emolt_sensor.SITE='
    dataset = get_dataset(url + '"' + site + '"')
    var = dataset['emolt_sensor']
    print 'extracting eMOLT data using PyDap... hold on'
    temp = list(var.TEMP)
    depth = list(var.DEPTH_I)
    time0 = list(var.YRDAY0_LOCAL)
    year_month_day = list(var.TIME_LOCAL)
    salt=list(var.SALT)
  
    print 'Generating a datetime ... hold on'
    datet = []
    for i in scipy.arange(len(time0)):
        #datet.append(num2date(time0[i]+1.0).replace(year=time.strptime(year_month_day[i], '%Y-%m-%d').tm_year).replace(day=time.strptime(year_month_day[i], '%Y-%m-%d').tm_mday))
        datet.append(num2date(time0[i]+1.0).replace(year=dt.datetime.strptime(year_month_day[i], '%Y-%m-%d').year).replace(month=dt.datetime.strptime(year_month_day[i],'%Y-%m-%d').month).replace(day=dt.datetime.strptime(year_month_day[i],'%Y-%m-%d').day).replace(tzinfo=None))
    #get the index of sorted date_time
    print 'Sorting mooring data by time'
    index = range(len(datet))
    index.sort(lambda x, y:cmp(datet[x], datet[y]))
    #reorder the list of date_time,u,v
    datet = [datet[i] for i in index]
    temp = [temp[i] for i in index]
    depth = [depth[i] for i in index]
    salt=[salt[i] for i in index]

    print 'Delimiting mooring data according to user-specified time'  
    part_t,part_time,part_salt = [], [],[]
    if len(input_time) == 2:
        start_time = input_time[0]
        end_time = input_time[1]
    if len(input_time) == 1:
        start_time = datet[0]
        end_time = start_time + input_time[0]
    if  len(input_time) == 0:
        start_time = datet[0]
        end_time=datet[-1]
    print datet[0], datet[-1]
    for i in range(0, len(temp)):
        if (start_time <= datet[i] <= end_time) & (dep[0]<=depth[i]<= dep[1]):
            part_t.append(temp[i])
            part_time.append(datet[i]) 
            part_salt.append(salt[i])
    temp=part_t
    datet=part_time
    salt=part_salt
    distinct_dep=np.mean(depth)
    return datet,temp,salt,distinct_dep






    




      
    




