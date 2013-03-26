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
the 5th line represent the sites you need, use "," to split
Sometimes data may be too larger than python limit, so you need to motify 6th line to 
split the date, and you also need to change the 2nd line to beginning one piece of whole date.
 
#######################

@author: huanxin
"""

import matplotlib.pyplot as plt
from matplotlib.dates import num2date,date2num
import sys
import os
#import numpy as np
ops=os.defpath

pydir='../'

sys.path.append(pydir)

from hx import getemolt_ctl
from hx import getemolt_sensor,getemolt_depth
from hx import colors,samesites_data
inputfilename='./getemolt_ctl.txt'

#get input use function "get_emolt_test_step"
(mindtime,maxdtime,i_mindepth,i_maxdepth,b_mindepth,b_maxdepth,lat_max,\
lon_max,lat_min,lon_min,site,num)=getemolt_ctl(inputfilename)   # get data from ctl file
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
      (time31,yrday301,temp31,sites31,depth_i,time1)=getemolt_sensor(mindtime1,\
      maxdtime1,i_mindepth,i_maxdepth,site2,mindtime,maxdtime)
      for p in range(len(sites31)):
          time1.append(time31[p])
          yrday01.append(yrday301[p])
          temp1.append(temp31[p])
          sites1.append(sites31[p])
          depth.append(depth_i[p])
      (sites32,depth_b1,lat_dd,lon_dd)=getemolt_depth(b_mindepth,b_maxdepth,lat_max,lon_max,lat_min,lon_min,site1)
      for q in range(len(sites32)):
          sites2.append(sites32[q])
          depth_b.append(depth_b1[q])

 
 
 
  (samesites,ave_temp,lat,lon)=samesites_data(sites1,sites2,temp1,lat_dd,lon_dd) #get samesites and average temp, latlon for point
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
            depth_b_same.append(depth_b[u])
   
      #when sensor close to bottom of sea
      temp11,yrday011,sites11,yrday0111,temp111,depth11=[],[],[],[],[],[]
      for j in range(len(sites1)):  
      
        if sites1[j]==samesites[k] and (abs(depth_b_same[0]-depth[j]))/float(depth_b_same[0])<0.2:   
            time11.append(time1[j])
            temp11.append(temp1[j])
            yrday011.append(yrday01[j])
            depth11.append(depth[j])
      for c in range(len(temp11)): #write and save data
          f.writelines(str(samesites[k])+str(lat[k])+'   '+str(lon[k])+'   '+str(depth11[c])+'   '+str(num2date(yrday011[c]).strftime('%Y,%m,%d,%H,%M'))+'   '+str(temp11[c])+'\n')
 
    
      #when sensor close to surface of sea
      temp11s,yrday011s,sites11s,yrday0111s,temp111s,depth11s=[],[],[],[],[],[]
      for l in range(len(sites1)):  
      
        if sites1[l]==samesites[k] and (abs(depth_b_same[0]-depth[l]))/float(depth_b_same[0])>=0.2:   
              time11.append(time1[l])
              temp11s.append(temp1[l])
              yrday011s.append(yrday01[l])
              depth11s.append(depth[l])
      for v in range(len(temp11s)):   #write and save data
        f.writelines(str(samesites[k])+'(s)  '+str(lat[k])+'   '+str(lon[k])+'   '+str(depth11s[v])+'   '+str(num2date(yrday011s[v]).strftime('%Y,%m,%d,%H,%M'))+'   '+str(temp11s[v])+'\n')
  mindtime=maxdtime
  maxdtime=num2date(date2num(maxdtime)+178)
f.close()