# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 10:09:30 2013

@author: jmanning
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from datetime import datetime
from pydap.client import open_url

def RungeKutta4_lonlat(lon,lat,Grid,u,v,tau):       
    lon1=lon*1.;          lat1=lat*1.;        urc1,v1=VelInterp_lonlat(lon1,lat1,Grid,u,v);  
    lon2=lon+0.5*tau*urc1;lat2=lat+0.5*tau*v1;urc2,v2=VelInterp_lonlat(lon2,lat2,Grid,u,v);
    lon3=lon+0.5*tau*urc2;lat3=lat+0.5*tau*v2;urc3,v3=VelInterp_lonlat(lon3,lat3,Grid,u,v);
    lon4=lon+    tau*urc3;lat4=lat+    tau*v3;urc4,v4=VelInterp_lonlat(lon4,lat4,Grid,u,v);
    lon=lon+tau/6.*(urc1+2.*urc2+2.*urc3+urc4);
    lat=lat+tau/6.*(v1+2.*v2+2.*v3+v4);       
    return lon,lat    
def nearxy(x,y,xp,yp):
    dx=x-xp
    dy=y-yp
    dist2=dx*dx+dy*dy
# dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    return i
def nearlonlat(lon,lat,lonp,latp):
    cp=np.cos(latp*np.pi/180.)
# approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
# dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    min_dist=np.sqrt(dist2[i])
    return i ,  min_dist  
def polygonal_barycentric_coordinates(xp,yp,xv,yv):
    N=len(xv)   
    j=np.arange(N)
    ja=(j+1)%N
    jb=(j-1)%N
    Ajab=np.cross(np.array([xv[ja]-xv[j],yv[ja]-yv[j]]).T,np.array([xv[jb]-xv[j],yv[jb]-yv[j]]).T)
    Aj=np.cross(np.array([xv[j]-xp,yv[j]-yp]).T,np.array([xv[ja]-xp,yv[ja]-yp]).T)
    Aj=abs(Aj)
    Ajab=abs(Ajab)
    Aj=Aj/max(abs(Aj))
    Ajab=Ajab/max(abs(Ajab))    
    w=xv*0.
    j2=np.arange(N-2)
    for j in range(N):
        w[j]=Ajab[j]*Aj[(j2+j+1)%N].prod()
      #  print Ajab[j],Aj[(j2+j+1)%N]
    w=w/w.sum()
    return w
def VelInterp_lonlat(lonp,latp,Grid,u,v):    
# find the nearest vertex    
    kv,distance=nearlonlat(Grid['lon'],Grid['lat'],lonp,latp)
#    print kv
# list of triangles surrounding the vertex kv    
    kfv=Grid['kfv'][0:Grid['nfv'][kv],kv]
#    print kfv
# coordinates of the (dual mesh) polygon vertices: the centers of triangle faces
    lonv=Grid['lonc'][kfv];latv=Grid['latc'][kfv] 
    w=polygonal_barycentric_coordinates(lonp,latp,lonv,latv)
# baricentric coordinates are invariant wrt coordinate transformation (xy - lonlat), check!    
#    print w
# interpolation within polygon, w - normalized weights: w.sum()=1.    
# use precalculated Lame coefficients for the spherical coordinates
# coslatc[kfv] at the polygon vertices
# essentially interpolate u/cos(latitude)
# this is needed for RungeKutta_lonlat: dlon = u/cos(lat)*tau, dlat = vi*tau
    cv=Grid['coslatc'][kfv]    
    urci=(u[kfv]/cv*w).sum()
    vi=(v[kfv]*w).sum()
        
    return urci,vi 
def rddate(TIME,numdays):    
    stime=datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
    timesnum=stime.year-1981
    standardtime=datetime.strptime(str(stime.year)+'-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
    timedeltaprocess=(stime-standardtime).days
    startrecord=26340+35112*(timesnum/4)+8772*(timesnum%4)+1+timedeltaprocess*24
    endrecord=startrecord+24*numdays
    return startrecord,endrecord,stime
def get_uv_web(time,layer):
        timeurl='['+str(time)+':1:'+str(time)+']'
        uvposition=str([layer])+'[0:1:90414]'
        url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'Times'+timeurl+',u'+timeurl+uvposition+','+'v'+timeurl+uvposition
        dataset = open_url(url)
        utotal=np.array(dataset['u'])
        vtotal=np.array(dataset['v'])
        times=np.array(dataset['Times'])
        u=utotal[0,0,:]
        v=vtotal[0,0,:]
        print times
        return u,v
TIME='1985-06-18 00:00:00' 
numdays=16
depth=0
behavior=0.005#1cm/s
#0.00000139#0.5cm/h
'''
fig=plt.figure(figsize=(7,6))
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,1),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,1),labels=[0,0,0,1])
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()
'''
startrecord,endrecord,stime=rddate(TIME,numdays)
url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'lon,lat,latc,lonc,siglay,h,x,y,xc,yc,nv,nbe,nbsn,ntsn,nbve,ntve,Times['+str(startrecord)+':1:'+str(endrecord)+']'
dataset = open_url(url)
latc = np.array(dataset['latc'])
lonc = np.array(dataset['lonc'])
lat = np.array(dataset['lat'])
lon = np.array(dataset['lon'])
x=np.array(dataset['x'])
y=np.array(dataset['y'])
xc=np.array(dataset['xc'])
yc=np.array(dataset['yc'])
nv=np.array(dataset['nv'])
nbe=np.array(dataset['nbe'])
nbsn=np.array(dataset['nbsn'])
ntsn=np.array(dataset['ntsn'])
nbve=np.array(dataset['nbve'])
ntve=np.array(dataset['ntve'])
siglay=np.array(dataset['siglay'])
h=np.array(dataset['h'])
coslat=np.cos(lat*np.pi/180.)
coslatc=np.cos(latc*np.pi/180.)
#################ready to process############################
Grid={'x':x,'y':y,'xc':xc,'yc':yc,'lon':lon,'lat':lat,'lonc':lonc,'latc':latc,'coslat':coslat,'coslatc':coslatc,'kvf':nv,'kff':nbe,'kvv':nbsn,'nvv':ntsn,'kfv':nbve,'nfv':ntve}
dt=60*60.
tau=dt/111111.
fig=plt.figure()    
#plt.plot(lon,lat,'r.',lonc,latc,'b+')
plt.title('vertical and behavior velocity '+' Time:'+TIME) 
FN='XY.npz'
Z=np.load(FN)
xlon=Z['X']
ylat=Z['Y']
#fig1=plt.figure(figsize=(7,6))
xi = np.arange(-69,-66.5,0.015)
yi = np.arange(40.,42.5,0.015)
firsttime=np.zeros((len(xi),len(yi)))
for nn in range(1,5):#(1,5)
     for n in range(0,20):#(0,20)
             lond=np.array([xlon[n,nn]])
             latd=np.array([ylat[n,nn]])
             print n,nn,lond,latd
             kf,distanceF=nearlonlat(lonc,latc,lond,latd) # nearest triangle center F - face
             kv,distanceV=nearlonlat(lon,lat,lond,latd)
             depthtotal=siglay[:,kv]*h[kv]
             layer=np.argmin(abs(depthtotal-depth))
             lont=[]
             latt=[]
             timerecord=[]
             depthfinal=[depth,]
             wdelta=0
             for i in range(startrecord+5,endrecord+5):    
                timeurl='['+str(i)+':1:'+str(i)+']'
                #uvposition=str([layer])+str([kf])
                uvposition=str([layer])+'[0:1:90414]'
                wposition=str([layer])+str([kv])
                url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'Times'+timeurl+',u'+timeurl+uvposition+','+'v'+timeurl+uvposition+','+'ww'+timeurl+wposition
                dataset = open_url(url)
                times=np.array(dataset['Times'])
                times=times[0][:19].replace("T"," ")
                eachtime=datetime.strptime(times[:13], "%Y-%m-%d %H")
                utotal=np.array(dataset['u'])
                vtotal=np.array(dataset['v']) 
                w=np.array(dataset['ww'])
                u=utotal[0,0,:]
                v=vtotal[0,0,:]
                w=w[0,0,0]
                if eachtime>datetime(eachtime.year, eachtime.month, eachtime.day, 0, 0) and eachtime<datetime(eachtime.year, eachtime.month, eachtime.day, 7, 0):
                   w=w+behavior
                   print "now is nighttime,shimp are swimming up"
                elif eachtime>=datetime(eachtime.year, eachtime.month, eachtime.day, 7, 0) and eachtime<=datetime(eachtime.year, eachtime.month, eachtime.day, 20, 0):
                   w=w-behavior
                   print "now is daylight, shimp are swimming down"
                else:
                   w=w+behavior
                   print "now is nighttime,shimp are swimming up"
                print "Time "+str(times)+','+"Layer "+str(layer)
################get the point according the position###################
                lont.append(lond[0])
                latt.append(latd[0])
                timerecord.append(i)
                lond,latd=RungeKutta4_lonlat(lond,latd,Grid,u,v,tau)
                wdelta=w*60*60+wdelta
                deptheach=depth+wdelta
    
                if deptheach>0:
                   deptheach=0
                   wdelta=0
                   depth=0
                if deptheach<-h[kv]:
                   deptheach=-h[kv]
                   wdelta=-h[kv]
                   depth=0
                depthfinal.append(deptheach)
                print w,deptheach,wdelta    
                kv,distance=nearlonlat(lon,lat,lond,latd)
                depthtotal=siglay[:,kv]*h[kv]
                layer=np.argmin(abs(depthtotal-deptheach))
                print lond,latd
                if distance>=0.3:
                   break
             plt.plot(lont,latt,'ro-',lont[0],latt[0],'mo')
             #plt.show()
             x=lont
             y=latt
             ix=np.digitize(x,xi)
             iy=np.digitize(y,yi)
             for mm in range(len(x)):
                    if (timerecord[mm]-startrecord)/24<=firsttime[ix[mm],iy[mm]] or firsttime[ix[mm],iy[mm]]==0:
                              firsttime[ix[mm],iy[mm]]=(timerecord[mm]-startrecord)/24        
                              print ix[mm],iy[mm],firsttime[ix[mm],iy[mm]]
             
             #Q=plt.contourf(xxb,yyb,firsttime)
             
xxb,yyb = np.meshgrid(xi, yi)
#firsttime[firsttime==0.0]=np.nan
Q=plt.contourf(xxb,yyb,firsttime.T)
b = plt.colorbar(Q, orientation='vertical')
plt.show()
#plt.savefig('depthtrend.png')



































