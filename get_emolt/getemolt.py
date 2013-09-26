# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 14:13:33 2012

@author: huanxin
"""

# -*- coding: utf-8 -*-
"""
######################
Notes
this use for get emolt data based on different conditions, It can be plot and save in file

The saving file will be in same floder as this program
When you running this program,you can select data and plot graphs according to 
your needs,you can create a file and open it.the file should be like this:

[1 0 0 0 1]
[2012,2,1,0,0;2012,2,2,0,0]
[10,200]
[20,200]
[4400,6880,3800,7400]
[PF01,DJ01]
[1]
The first line represent index of the following 5 line,'1' means picking,'0' means not.
the 2nd line represent the period of date
the 3rd line represent the range depth of sensor
the 4th line represent the range depth of bottom
the 5th line represent the range lat,lon of range:maxlat,maxlon,minlat,minlon
the 6th line represent the sites you need, use "," to split
the 7th line represent the number of times to split the data
Sometimes data may be too larger than python limit, so you need to motify 6th line to 
split the date, and you also need to change the 2nd line to beginning one piece of whole date.
 
#######################

@author: huanxin
"""

import matplotlib.pyplot as plt
from matplotlib.dates import num2date,date2num
import sys
import os
import datetime as dt
from pydap.client import open_url
import numpy as np
##JiM change
from pandas import DataFrame
#import numpy as np
ops=os.defpath

pydir='../'

sys.path.append(pydir)

#from hx import getemolt_ctl
from hx import getemolt_sensor,getemolt_depth
from hx import colors,samesites_data
inputfilename='./getemolt_ctl.txt'

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
       mindtime=dt.datetime.strptime('2001,1,1,0,0','%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime('2013,4,2,0,0','%Y,%m,%d,%H,%M')
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
       ### JiM change
       lon_max=8000  
       lat_min=3000
       lon_min=5000
       
if select5 =='1':
       site=f.readline()
       site=site[0:site.index(']')].strip('[').split(',') 
else:
       site=f.readline()
       site=''

num=f.readline()
num=int(num[0:num.index(']')].strip('['))    
#get input use function "get_emolt_test_step"
#(mindtime,maxdtime,i_mindepth,i_maxdepth,b_mindepth,b_maxdepth,lat_max,lon_max,lat_min,lon_min,site,num)=getemolt_ctl(inputfilename)   # get data from ctl file
#change format of date to get datetime format
f = open(str(int(lat_min))+'.txt', 'w')
f.writelines('site'+'      '+'lat      '+' lon     '+' depth'+'  '+'     time'+'          '+'temp(F)'+'\n')
for aaa in range(num):
# number pieces of date   
   mindtime1=mindtime.strftime("%d-%b-%Y")
   maxdtime1=num2date((date2num(maxdtime))+1).strftime("%d-%b-%Y") #we need to add 1 day,because start time of one day is 00:00
   maxdtime11=maxdtime.strftime("%d-%b-%Y")
  #when user don't input sites,get data from url
   if site=='':
      site2=''
      site1=''
      (sites2,depth_b,lat_dd,lon_dd)=getemolt_depth(b_mindepth,b_maxdepth,lat_max,\
      lon_max,lat_min,lon_min,site1)
    
      (time1,yrday01,temp1,sites1,depth)=getemolt_sensor(mindtime1,\
      maxdtime1,i_mindepth,i_maxdepth,site2,mindtime,maxdtime)

  #when user input sites,get data from url,change their format 
   else:   
        time1,yrday01,temp1,sites1,sites2,depth_b,depth=[],[],[],[],[],[],[]
        for o in range(len(site)):
      # change site format for using it in url
            site1='&emolt_site.SITE="'+site[o]+'"'
            site2='&emolt_sensor.SITE="'+site[o]+'"'


            url2="http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.TIME_LOCAL,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I&emolt_sensor.TIME_LOCAL>="+str(mindtime1)+"&emolt_sensor.TIME_LOCAL<="+str(maxdtime1)+"&emolt_sensor.DEPTH_I>="+str(i_mindepth)+"&emolt_sensor.DEPTH_I<="+str(i_maxdepth)+site2         
            dataset1=open_url(url2)
            emolt_sensor=dataset1['emolt_sensor']
            sites2=list(emolt_sensor['SITE'])
            time=list(emolt_sensor['TIME_LOCAL'])
            yrday0=list(emolt_sensor['YRDAY0_LOCAL'])
            temp=list(emolt_sensor['TEMP'])
            depth1=list(emolt_sensor['DEPTH_I'])
	
	
            time31,temp31,yrday301,sites31,depth_i=[],[],[],[],[]
            for m in range(len(time)):
	      #if mindtime<=dt.datetime.strptime(str(time[m]),'%Y-%m-%d')<=maxdtime:
	      if date2num(mindtime)<=yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))<=date2num(maxdtime):
	      #if str(time[m])=='2012-01-01':
	        temp31.append(temp[m])
	        yrday301.append(yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d')))
	        sites31.append(sites2[m])
	        time31.append(date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))) 
	        depth_i.append(depth1[m])   
            for p in range(len(sites31)):
                  time1.append(time31[p])
                  yrday01.append(yrday301[p])
                  temp1.append(temp31[p])
                  sites1.append(sites31[p])
                  depth.append(depth_i[p])
           
           
            url="http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE,emolt_site.BTM_DEPTH,emolt_site.LAT_DDMM,emolt_site.LON_DDMM&emolt_site.BTM_DEPTH<="+str(b_maxdepth)+"&emolt_site.BTM_DEPTH>="+str(b_mindepth)+"&emolt_site.LON_DDMM<="\
            +str(lon_max)+"&emolt_site.LON_DDMM>="+str(lon_min)+"&emolt_site.LAT_DDMM<="+str(lat_max)+"&emolt_site.LAT_DDMM>="+str(lat_min)+site1
            try:   
	           dataset=open_url(url)
            except:
	           print 'Sorry, '+url+' not available' 
	           sys.exit(0)
            emolt_site=dataset['emolt_site']
            sites32=list(emolt_site['SITE'])
            depth_b1=list(emolt_site['BTM_DEPTH'])        
            lat_dd=list(emolt_site['LAT_DDMM'])
            lon_dd=list(emolt_site['LON_DDMM'])
            for q in range(len(sites32)):
                  sites2.append(sites32[q])
                  depth_b.append(depth_b1[q])

 
 
 
   samesites=list(set(sites2).intersection(set(sites1)))
   if samesites==[]:
      print "Can not find eligible data, please re-enter the conditions"
      sys.exit(0)
    
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
              ### 
              #lat.append(lat_dd[z])
              #lon.append(lon_dd[z])  
              lat.append(lat_dd)
              lon.append(lon_dd)  
   samesites=samesites0
   ave_temp=ave_temp0
   
   
   
   
   
   
  # plot more colors with function "uniquecolors"    
   n=int(len(samesites))+2 #how many colors
   (rgbcolors)=colors(n)

   fig = plt.figure()
   ax = fig.add_subplot(111)
  # data in same site, plot in one line
   time11=[]
 
   for k in range(len(samesites)):
      #According samesites, get bottom depth
      depth_b_same=[]
      for u in range(len(sites2)):     
        if sites2[u]==samesites[k]:
            #depth_b_same.append(depth_b[u])
            depth_b_same.append(depth_b)
   
      #when sensor close to bottom of sea
      temp11,yrday011,sites11,yrday0111,temp111,depth11=[],[],[],[],[],[]
      for j in range(len(sites1)):  
      
        # JiM change 7/6/13
        #if sites1[j]==samesites[k] and (abs(depth_b_same[0]-depth[j]))/float(depth_b_same[0])<0.2:   
        if sites1[j]==samesites[k] and (abs(depth_b_same[0]-depth[j]))/float(depth_b_same[0][0])<0.2:   
            time11.append(time1[j])
            temp11.append(temp1[j])
            yrday011.append(yrday01[j])
            depth11.append(depth[j])
      dtt=[]      
      for c in range(len(temp11)): #write and save data
          f.writelines(str(samesites[k])+str(lat[k])+'   '+str(lon[k])+'   '+str(depth11[c])+'   '+str(num2date(yrday011[c]).strftime('%Y,%m,%d,%H,%M'))+'   '+str(temp11[c])+'\n')
    
      #when sensor close to surface of sea
      temp11s,yrday011s,sites11s,yrday0111s,temp111s,depth11s=[],[],[],[],[],[]
      for l in range(len(sites1)):  
      
        #if sites1[l]==samesites[k] and (abs(depth_b_same[0]-depth[l]))/float(depth_b_same[0])>=0.2:   
        # What is this "0.2" parameter?    
        if sites1[l]==samesites[k] and (abs(depth_b_same[0]-depth[l]))/float(depth_b_same[0][0])>=0.2:   
              time11.append(time1[l])
              temp11s.append(temp1[l])
              yrday011s.append(yrday01[l])
              depth11s.append(depth[l])
      for v in range(len(temp11s)):   #write and save data
        f.writelines(str(samesites[k])+'(s)  '+str(lat[k])+'   '+str(lon[k])+'   '+str(depth11s[v])+'   '+str(num2date(yrday011s[v]).strftime('%Y,%m,%d,%H,%M'))+'   '+str(temp11s[v])+'\n')

   mindtime=maxdtime
   ## JiM changed comment
   maxdtime=num2date(date2num(maxdtime)+178)# Note: we are adding 178 days here since that is the limit of our OPENDAP server and we need to step through that many days
f.close()