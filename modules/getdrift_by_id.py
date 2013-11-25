 # -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 10:30:10 2012

@author: huanxin
modified by JiM in May and again Nov 2013

Routine to plot drifter tracks given just "id"

Two figures are made after a OPeNDAP call to "getdrift":
1) plain track 
2) plain track with speed colorcoded

Uses modules "getdata" and "drifter" where it finds functions:
"getdrift, plot_latlon, calculate_speedcolors, plot_speedcolors" 
"""

import getdata
from drifter import plot_latlon,calculate_speedcolors,plot_speedcolors
from basemap import basemap_usgs
import matplotlib.pyplot as plt

import pylab
#id=raw_input("please input id,(example: 115361221 ): ")
ids=[55201,55202,55203]
#linecol=['red','green','blue']
linecol=['green','red','blue']
ndays_label=10

#basemap_JiM([40,43],[-72,-67],False,False)
basemap_usgs([40.25,43],[-72,-67],True,True)


for k in range(len(ids)):
  #get lat,lon,time use function "getdrift"
  (lat,lon,datet,dep)=getdata.getdrift(ids[k])

  #plot lat,lon, and add text of time in the figure
  if ids[k]==55201:
      daymth=['5/10','5/21','5/22','7/3','7/16']
  elif ids[k]==55202:
      daymth=['5/10','5/22','6/1','6/10']
  elif ids[k]==55203:
      daymth=['5/18','6/1','6/10']

  plot_latlon(lat,lon,datet,ids[k],ndays_label,linecol[k],daymth)

plt.text(-71.95,42.8,'NewHampshire',color='white',fontweight='bold')
plt.text(-71.95,42.15,'Massachusetts',color='white',fontweight='bold')
plt.text(-71.95,41.8,'Rhode Island',color='white',fontweight='bold')
plt.text(-68.5,40.8,'Georges Bank',color='black',rotation=20,fontweight='bold')
plt.ylim(40.25,43)
plt.xlim(-72,-67)
plt.show()

#plot lat,lon,speed and add text of time in the figure
#(speed,speed_color)=calculate_speedcolors(lat,lon,datet)
# this function is in drifter
#plot_speedcolors(id,speed,datet,speed_color,lat,lon,4)# this function is in drifter
