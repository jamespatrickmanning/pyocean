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
from conversions import dm2dd,f2c
import pandas as pd
from numpy import float32
import os
site='AB01'
# get data
[lati,loni,on,bd]=getemolt_latlon(site)# extracts lat/lon based on site code
[lati,loni]=dm2dd(lati,loni)#converts decimal-minutes to decimal degrees
'''
dept=[0,5]
(obs_dt,obs_temps,obs_salt)=getobs_tempsalt(site, input_time=[dt.datetime(2004,6,7),dt.datetime(2004,6,24)], dep=dept)
obs_tempslist=[]
for i in range(len(obs_temps)):
         obs_tempslist.append(f2c(obs_temps[i]))
dfsur=pd.DataFrame(obs_tempslist,index=obs_dt)
'''
dept=[bd[0]-0.4*bd[0],bd[0]+0.35*bd[0]]
(obs_dt,obs_tempb,obs_salt)=getobs_tempsalt(site, input_time=[dt.datetime(2004,6,7),dt.datetime(2004,6,24)], dep=dept)
obs_tempblist=[]
for i in range(len(obs_tempb)):
         obs_tempblist.append(f2c(obs_tempb[i]))
dfbot=pd.DataFrame(obs_tempblist,index=obs_dt)
#dfsur=dfsur.ix[dfsur.index.hour==0]
#dfbot=dfbot.ix[dfbot.index.hour==0]
# get model

modtso=getFVCOM_bottom_tempsalt_netcdf(lati,loni,dt.datetime(2004,6,7),dt.datetime(2004,6,24),layer=range(45),vname='temp')
#modtso=modtso.ix[modtso.index.hour==0] 
for i in range(len(dfbot)):
    fig=plt.figure()
    plt.plot(modtso.values[i],range(0,-45,-1),'g*')
#    plt.plot([float32(dfsur[0][i]),float32(dfbot[0][i])],[0,-44],'r*')
    plt.plot([float32(dfbot[0][i])],[-44],'r*')
    plt.ylim(-45,1)
    plt.xlabel('layer(0-44)')
    plt.ylabel('Temprature(Centigrade)')
    plt.title(site+' '+str(modtso.index[i]))
    plt.xlim(4.7,16.5)
    filename = str('%03d' % i) + '.png'
    plt.savefig('/net/home3/ocn/jmanning/py/mygit/modules/tempfigures/'+filename)    
    if i <=10:
        plt.show()
#    plt.plot(modtso[0],-k,'g*')
#plt.plt([obs_temps[0],obs_tempb[0]],[0,-bd[0]],'r*') 

anim_name ='surbottempAB01.flv'
    
    #cmd = 'c:\\ffmpeg\\ffmpeg.exe -i c:\\Python26\\animations\\%03d.png -r 15 -b 614000 c:\\Python26\\done\\' + anim_name
#cmd = 'ffmpeg -i /home3/ocn/jmanning/py/mygit/modules/tempfigure/%03d.png -r 20 -b 614000 /net/nwebserver/drifter/anim/' + anim_name 
cmd = 'ffmpeg -i /net/home3/ocn/jmanning/py/mygit/modules/tempfigures/%03d.png -r 7 -b 614000 /net/home3/ocn/jmanning/py/mygit/modules/tempfigures/' + anim_name
os.system(cmd)
print "success"