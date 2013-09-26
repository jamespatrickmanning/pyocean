# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:23:37 2012

@author: Huanxin
"""
import math
import matplotlib
import scipy
import datetime
import numpy
import matplotlib.pyplot as plt
from matplotlib.dates import num2date,date2num
from matplotlib.dates import  DateFormatter
import datetime as dt
import pylab
from pydap.client import open_url
import sys
#pydir='/net/home3/ocn/jmanning/py/huanxin/work'
import numpy as np
import matplotlib.mlab as ml
import time
import pytz
utc = pytz.timezone('UTC')
#sys.path.append(pydir)


def colors(n):
	  """Compute a list of distinct colors, each of which is represented as an RGB 3-tuple."""
	  """It's useful for less than 100 numbers"""
	  if pow(n,float(1)/3)%1==0.0:
	     n+=1 
	  #make sure number we get is more than we need.
	  rgbcolors=[]
	  x=pow(n,float(1)/3)
	  a=int(x)
	  b=int(x)
	  c=int(x)
	  if a*b*c<=n:
	    a+=1
	  if a*b*c<n:
	    b+=1
	  if a*b*c<n:
	    c+=1
	  for i in range(a):
	      r=0.99/(a)*(i)
	      for j in range(b):
	          s=0.99/(b)*(j)
	          for k in range(c):
	              t=0.99/(c)*(k)
	              color=r,s,t
	              rgbcolors.append(color)
	  return rgbcolors


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
      temp_ave=np.mean(temp_a)
      ave_temp.append(temp_ave)
    c=zip(samesites,ave_temp)
    d=sorted(c, key=lambda c: c[1])
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

def getcodar(url,id):
  id=str(id)
  dataset=open_url(url+'?u['+id+':1:'+id+'][0:1:128][0:1:137],v['+id+':1:'+id+'][0:1:128][0:1:137],lat[0:1:128],lon[0:1:137]')
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
  interval_dtime=datetime.timedelta( 0,interval*60*60 )

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
    #print 'the index edge for codar is  '+lat_max_i,lat_min_i,lon_max_i,lon_min_i
    return lat_max_i,lon_max_i,lat_min_i,lon_min_i
def getcodar_ctl_id(model_option,url,datetime_wanted):
    if model_option=='1':
        dtime=open_url(url+'?time')
        dd=dtime['time']  
        #print "This option has data from "+str(num2date(dd[0]+date2num(datetime.datetime(2009, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(datetime.datetime(2009, 1, 1, 0, 0))))           
        print 'This option has data from '+dd[0].strftime("%B %d, %Y")+' to '+dd[-1] .strftime("%B %d, %Y")
        id=datetime_wanted-date2num(datetime.datetime(2009, 1, 1, 0, 0))
        id=str(int(id))
    else:
        dtime=open_url(url+'?time')
        dd=dtime['time']
        ddd=[]
        for i in list(dtime['time']):
            i=round(i,7)
            ddd.append(i)
        
        #print "This option has data from "+str(num2date(dd[0]+date2num(datetime.datetime(2001, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(datetime.datetime(2001, 1, 1, 0, 0)))) 
        #print 'This option has data from '+num2date(dd[0]).strftime("%B %d, %Y")+' to '+num2date(dd[-1]).strftime("%B %d, %Y")          
        id=ml.find(np.array(ddd)==round(datetime_wanted-date2num(datetime.datetime(2001, 1, 1, 0, 0)),7))
        for i in id:
          id=str(i) 
        #print 'codar id is  '+id
    return id    
#print id1
#id=date2num(datetime_wanted)-date2num(datetime.datetime(2009, 1, 1, 0, 0))
def basemap_usgs(lat,lon,bathy):
    # plot the coastline and, if bathy is True, bathymetry is plotted
    # lat and lon can be any list of positions in decimal degrees
    # does NOT need a copy og third party Basemap to be installed

    url='http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v03'
    def get_index_latlon(url):# use the function to calculate the minlat,minlon,maxlat,maxlon location
        try:
          dataset=open_url(url)
        except:
          print "please check your url!"
          #sys.exit(0)
        basemap_lat=dataset['lat']
        basemap_lon=dataset['lon']
        basemap_topo=dataset['topo']
    
        # add the detail of basemap
        minlat=min(lat)-0.01
        maxlat=max(lat)+0.01
        minlon=min(lon)+0.01
        maxlon=max(lon)-0.01
        index_minlat=int(round(np.interp(minlat,basemap_lat,range(0,basemap_lat.shape[0]))))
        index_maxlat=int(round(np.interp(maxlat,basemap_lat,range(0,basemap_lat.shape[0]))))

        index_minlon=int(round(np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        index_maxlon=int(round(np.interp(maxlon,basemap_lon,range(0,basemap_lon.shape[0]))))

        #print np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))
        #print index_minlon
        return index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo
    
    index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo = get_index_latlon(url)
    min_index_lat=min(index_minlat,index_maxlat)
    max_index_lat=max(index_minlat,index_maxlat)
    min_index_lon=min(index_minlon,index_maxlon)
    max_index_lon=max(index_minlon,index_maxlon)
    if index_maxlat-index_minlat==0 or index_maxlon-index_minlon==0:
        
        url='http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc'
        try:
          dataset=open_url(url)
        except:
          print "please check your url!"
          sys.exit(0)
        basemap_lat=dataset['lat']
        basemap_lon=dataset['lon']
        basemap_topo=dataset['topo']
        # add the detail of basemap
        minlat=min(lat)-0.01
        maxlat=max(lat)+0.01
        minlon=min(lon)+0.01
        maxlon=max(lon)-0.01
        basemap_lat=[float(i) for i in basemap_lat]
        basemap_lat_r=sorted(basemap_lat)
       # basemap_lat.reverse()
   
        range_basemap_lat=range(len(basemap_lat))
        range_basemap_lat.reverse()
        index_minlat=int(round(np.interp(minlat,basemap_lat_r,range_basemap_lat)))
        index_maxlat=int(round(np.interp(maxlat,basemap_lat_r,range_basemap_lat)))




        index_minlon=int(round(np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        index_maxlon=int(round(np.interp(maxlon,basemap_lon,range(0,basemap_lon.shape[0]))))

        # index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo = get_index_latlon(url)
        min_index_lat=min(index_minlat,index_maxlat)
        max_index_lat=max(index_minlat,index_maxlat)
        min_index_lon=min(index_minlon,index_maxlon)
        max_index_lon=max(index_minlon,index_maxlon) 
 
    
    X,Y=np.meshgrid(basemap_lon[min_index_lon:max_index_lon],basemap_lat[min_index_lat:max_index_lat])

    # You can set negative contours to be solid instead of dashed:
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    # plot the depth
    #print index_minlat,index_maxlat
    #plt.xlim([min(lon),max(lon)])
    #plt.ylim([min(lat),max(lat)])
    #plot the bathy
    if bathy==True:
        CS=plt.contour(X,Y,basemap_topo.topo[min_index_lat:max_index_lat,index_minlon:index_maxlon],3,colors=['gray','green'],linewith=0.05)
        plt.clabel(CS, fontsize=7,fmt='%5.0f', inline=1)
    #plt.clabel(cs, fontsize=9, inline=1,fmt='%5.0f'+"m")
    plt.contourf(X,Y,basemap_topo.topo[min_index_lat:max_index_lat,min_index_lon:max_index_lon],[0,1000],colors='grey')
def getsst(ask_input):
    #get the index of second from the url
    #time_tuple=time.gmtime(second[0])#calculate the year from the seconds
      #change the datetime to seconds
    ask_datetime=ask_input.replace(tzinfo=utc)
    timtzone_ask_datetime=ask_datetime.astimezone(utc)
    second=time.mktime(timtzone_ask_datetime.timetuple())
    time_tuple=time.gmtime(second)#calculate the year from the seconds
    year=time_tuple.tm_year
    print "year="+str(year)
    if (year<1999) or (year>2011):
      print 'Using new RUTGERS server for '+str(year)
      url1='http://tds.maracoos.org/thredds/dodsC/SST-Three-Agg.nc'
    else:    
      url1='http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/'+str(year)+'?time[0:1:3269]'
    dataset1=open_url(url1)
    times=list(dataset1['time'])
    # find the nearest image index
    index_second=int(round(numpy.interp(second,times,range(len(times)))))
    


    #get sst, time, lat, lon from the url
    #if (year>=1999) and (year<=2011):
    #    url='http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/avhrr/bigbight/'+str(year)+'?lat[0:1:3660],lon[0:1:4499],'+'mcsst['+str(index_second)+':1:'+str(index_second)+'][0:1:3660][0:1:4499]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    #else:
    url='http://tds.maracoos.org/thredds/dodsC/SST-Three-Agg.nc?lat[0:1:3660],lon[0:1:4499],'+'mcsst['+str(index_second)+':1:'+str(index_second)+'][0:1:3660][0:1:4499]'+',time['+str(index_second)+':1:'+str(index_second)+']'
    try:
        print url
        dataset=open_url(url)
    except:
        print "please check your url!"
        sys.exit(0)

    sst=dataset['mcsst'].mcsst
    time1=dataset['time']
    lat=dataset['lat']
    lon=dataset['lon']
    return sst,time1,lat,lon,index_second

def plot_getsst(ask_input,utc,gbox):
  # where ask_imput is day you want(the format is 2009-08-01 18:34:00)
  # where utc is usually 'utc'
  # where gbox is, for example, [-71, -70.5, 41.25, 41.75]
  #sys.path.append('/net/home3/ocn/jmanning/py/jmanning/whython5/oceanography/')

  #from getdata import getsst

  #year=dt.datetime.strptime(ask_input,'%Y-%m-%d %H:%M:%S').year
  
  sst,time1,lat,lon,index_second=getsst(ask_input)

  # find the index for the gbox
  index_lon1=int(round(numpy.interp(gbox[0],list(lon),range(len(list(lon))))))
  index_lon2=int(round(numpy.interp(gbox[1],list(lon),range(len(list(lon))))))
  index_lat1=int(round(numpy.interp(gbox[2],list(lat),range(len(list(lat))))))
  index_lat2=int(round(numpy.interp(gbox[3],list(lat),range(len(list(lat))))))
  # get part of the sst
  #print index_lon1,index_lon2,index_lat1,index_lat2,np.shape(sst),gbox
  sst_part=sst[index_second,index_lat1:index_lat2,index_lon1:index_lon2]
  #print sst_part
  print np.shape(sst_part)

  sst_part[(sst_part==-999)]=numpy.NaN # if sst_part=-999, convert to NaN
  #sst_part[numpy.isnan(sst_part)]=0 # then change NaN to 0
  X,Y=numpy.meshgrid(lon[index_lon1:index_lon2],lat[index_lat1:index_lat2])
  #plot
  plt.figure()
  # get the min,max of lat and lon
  '''
  minlat=min(lat[index_lat1:index_lat2])
  maxlat=max(lat[index_lat1:index_lat2])
  minlon=min(lon[index_lon1:index_lon2])
  maxlon=max(lon[index_lon1:index_lon2])
  '''
  # plot the basemap
  #basemap_usgs([minlat,maxlat],[minlon,maxlon],False,)
  #basemap_standard([minlat,maxlat],[minlon,maxlon],[3])
  #basemap_region('sne')
  # plot the temperature
  #print sst_part[0],np.nanmin(sst_part[0]),np.nanmax(sst_part[0])
  #CS = plt.contourf(X,Y,sst_part[0],np.arange(22.,26.,.25))
  
  mi=np.nanmin(sst_part[0])
  ma=np.nanmax(sst_part[0])
  rg=ma-mi
  mi=mi+rg*0.5 # adds 50 % of the range to account for cold cloud like pixels
  #CS = plt.contourf(X,Y,sst_part[0],np.arange(mi,ma,(ma-mi)/12.))
  CS = plt.contourf(X,Y,sst_part[0],np.arange(np.nanmin(sst_part[0])+2.0,np.nanmax(sst_part[0]),(np.nanmax(sst_part[0])-(np.nanmin(sst_part[0])+2.0))/6.))
  plt.colorbar(CS,format='%4.1f'+'C')

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
  print 'number of frames, interval time (hours), step size (hours?) :'+str(num_interval)
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=datetime.timedelta( 0,interval*60*60 )
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

def getdrift_raw(filename,id3,interval,datetime_wanted):
    
  # range_time is a number,unit by one day.  datetime_wanted format is num
  d=ml.load(filename)
  lat1=d[:,8]
  lon1=d[:,7]
  idd=d[:,0]
  year=[]
  for n in range(len(idd)):
      year.append(str(idd[n])[0:2])
  h=d[:,4]
  day=d[:,3]
  month=d[:,2]
  time1=[]
  for i in range(len(idd)):
      time1.append(date2num(datetime.datetime.strptime(str(int(h[i]))+' '+str(int(day[i]))+' '+str(int(month[i]))+' '+str(int(year[i])), "%H %d %m %y")))


  idg1=list(ml.find(idd==id3))
  idg2=list(ml.find(np.array(time1)<=datetime_wanted+interval/24))
  "'0.25' means the usual Interval, It can be changed base on different drift data "
  idg3=list(ml.find(np.array(time1)>=datetime_wanted-0.1))
  idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
  idg=list(set(idg23).intersection(set(idg1)))
  print 'the length of drifter data is  '+str(len(idg)),str(len(set(idg)))+'   . if same, no duplicate'
  lat,lon,time=[],[],[]
  
  for x in range(len(idg)):
      lat.append(round(lat1[idg[x]],4))
      lon.append(round(lon1[idg[x]],4))
      time.append(round(time1[idg[x]],4))
  # time is num
  return lat,lon,time

def getdrift_raw_range_latlon(filename,id3,interval,datetime_wanted_1,num,step_size):
    
# this is for plot all the data in same range of lat and lon. id3 means int format of drift number
#'interval' means range of time, 'num' means how many pictures we will get
  d=ml.load(filename)
  
  lat1=d[:,8]
  lon1=d[:,7]
  idd=d[:,0]
  year=[]
  for n in range(len(idd)):
      year.append(str(idd[n])[0:2])
  h=d[:,4]
  day=d[:,3]
  month=d[:,2]
  time1=[]
  for i in range(len(idd)):
      time1.append(date2num(datetime.datetime.strptime(str(int(h[i]))+' '+str(int(day[i]))+' '+str(int(month[i]))+' '+str(int(year[i])), "%H %d %m %y")))


  idg1=list(ml.find(idd==id3))
  idg2=list(ml.find(np.array(time1)<=datetime_wanted_1+step_size/24.0*(num-1)+0.25))
  "'0.25' means the usual Interval, It can be changed base on different drift data "
  idg3=list(ml.find(np.array(time1)>=datetime_wanted_1-interval/24.0))
  idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
  idg=list(set(idg23).intersection(set(idg1)))
 # print len(idg),len(set(idg))  
  lat,lon,time=[],[],[]
  
  for x in range(len(idg)):
      lat.append(round(lat1[idg[x]],4))
      lon.append(round(lon1[idg[x]],4))
  maxlon=max(lon)
  minlon=min(lon)
  maxlat=max(lat)
  minlat=min(lat)     
  # time is num
  return maxlon,minlon,maxlat,minlat
