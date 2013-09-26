 # -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 10:30:10 2012

@author: huanxin
modified by JiM in May 2013

Routine to plot drifter tracks given just "id"

Two figures are made after a OPeNDAP call to "getdrift":
1) plain track 
2) plain track with speed colorcoded

Uses modules "getdata" and "drifter" where it finds functions:
"getdrift, plot_latlon, calculate_speedcolors, plot_speedcolors" 
"""

from getdata import getdrift
from drifter import plot_latlon,calculate_speedcolors,plot_speedcolors
from datetime import datetime as dt

#id=raw_input("please input id,(example: 115361221 ): ")
id='115361221'

#get lat,lon,time use function "getdrift"
#(lat,lon,datet,dep)=getdrift(id)


lat=[40.0,40.4,40.5,40.7,40.75]
lon=[70.,70.,70.,70.,70.]
year=2013
datet=[dt(year,1,1,0,0,0),dt(year,1,2,0,0,0),dt(year,1,3,0,0,0),dt(year,1,4,0,0,0),dt(year,1,5,0,0,0)]

#plot lat,lon, and add text of time in the figure
plot_latlon(lat,lon,datet,id)
#plot lat,lon,speed and add text of time in the figure
(speed,speed_color)=calculate_speedcolors(lat,lon,datet)
# this function is in drifter
plot_speedcolors(id,speed,datet,speed_color,lat,lon,4)# this function is in drifter
