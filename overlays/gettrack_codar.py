# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:07:30 2012

@author:huanxin
"""
"""
based on codar data, simulate drifter track and plot it
"""
import sys
from  matplotlib.dates import num2date
import pylab
import matplotlib.pyplot as plt
# add the path of ocean.py
#pydir='/net/home3/ocn/jmanning/py/huanxin/work'

#sys.path.append(pydir)

from hx import getcodar_ctl_file,getdrift_raw_range_latlon,getcodar_ctl_id
from hx import getdrift_raw,getcodar,gettrack_codar    
#### input #########################################################
inputfilename='getcodar_bydrifter_ctl.txt'
(datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size)=getcodar_ctl_file(inputfilename)
startdate=datetime_wanted

id3=int(driftnumber)  #change format
datetime_wanted_1=datetime_wanted
(maxlon,minlon,maxlat,minlat)=getdrift_raw_range_latlon(filename,id3,interval,datetime_wanted_1,num,step_size)

id=getcodar_ctl_id(model_option,url,startdate)
(lat,lon,time)=getdrift_raw(filename,id3,interval,datetime_wanted) #drifter lat lon time
la=lat[0]
lo=lon[0]
lat_k,lon_k=[la],[lo]
uu,vv=[0],[0]
for q in range(interval):
    lat_vel,lon_vel,u,v=getcodar(url,id)
    lon_vel_list=lon_vel[0]
    lat_vel_list=[]
    for g in range(len(lat_vel)):
        lat_vel_list.append(lat_vel[g][0])
       
    lat_k1,lon_k1,time1,uu,vv=gettrack_codar(lon_vel_list,lat_vel_list,u,v,startdate,interval,la,lo,uu,vv,q)
    la=lat_k1
    lo=lon_k1
    lat_k.append(lat_k1)
    lon_k.append(lon_k1)
    print str(q)
    id=str(int(id)+1)   #the interval is 1 hour
#maxlat=max(lat_k);minlat=min(lat_k);maxlon=max(lon_k);minlon=min(lon_k)
#find the edge

for i in range(5):
    if maxlat-minlat<=0.1:
        maxlat=maxlat+0.01
        minlat=minlat-0.01
    if maxlon-minlon<=0.1:
        maxlon=maxlon+0.01
        minlon=minlon-0.01# make plotting lat lon as usual,not too small

pylab.ylim([minlat-0.02,maxlat+0.02])
pylab.xlim([minlon-0.02,maxlon+0.02])
#plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)))

plt.plot(lon_k[0],lat_k[0],'.',markersize=20,color='g',label='start')  #plot end and start
plt.plot(lon_k[-1],lat_k[-1],'.',markersize=20,color='r',label='end')
plt.plot(lon_k,lat_k,"-",linewidth=1,marker=".",markerfacecolor='r')
plt.legend( numpoints=1)
plt.title('from '+num2date(startdate).strftime("%d/%m/%y %H")+'h   to   '+num2date(startdate+interval/24.0).strftime("%d/%m/%y %H")+'h')
plt.show()
plt.savefig('./expect_drifter.png')
#print "past getcodar call with first time = "+str(jdmat_m[0])+" first u = "+str(u[0][0])
#fig=plt.figure(1)
#idg=list(np.where(u[0]<>-999.0/100.)[0])
#q=plt.quiver(lon_vel[idg],lat_vel[idg],u[0][idg],v[0][idg],angles='xy',scale=10,color='r')
#plt.plot(lo,la,'k.',markersize=30)
