# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:20:47 2013
Routine to look at model temperature profiles 
ar a particular eMOLT location where we had both surf & bot sensors
@author: jmanning

"""
import datetime as dt
from matplotlib import pyplot as plt
from getdata_yw import getobs_tempsalt
from getdata import getemolt_latlon
from models_yw import getFVCOM_bottom_tempsalt_netcdf
from conversions import dm2dd
import pandas as pd

site='AG01'
# get data
[lati,loni,on,bd]=getemolt_latlon(site)# extracts lat/lon based on site code
[lati,loni]=dm2dd(lati,loni)#converts decimal-minutes to decimal degrees
dept=[0,5]
(obs_dt,obs_temps,obs_salt)=getobs_tempsalt(site, input_time=[dt.datetime(2006,9,10),dt.datetime(2006,10,11)], dep=dept)
dfsur=pd.DataFrame(obs_temps,index=obs_dt)
dept=[bd[0]-0.25*bd[0],bd[0]+0.25*bd[0]]
(obs_dt,obs_tempb,obs_salt)=getobs_tempsalt(site, input_time=[dt.datetime(2006,9,10),dt.datetime(2006,10,11)], dep=dept)
dfbot=pd.DataFrame(obs_tempb,index=obs_dt)
'''# get model
for k in range(44):
    modtso=getFVCOM_bottom_tempsalt_netcdf(lati,loni,dt.datetime(2006,9,10),dt.datetime(2006,9,11),layer=k,vname='temp') 
    plt.plot(modtso[0],-k,'g*')
plt.plt([obs_temps[0],obs_tempb[0]],[0,-bd[0]],'r*') 
'''
