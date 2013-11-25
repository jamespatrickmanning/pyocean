# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 10:09:30 2013

@author: jmanning
"""

import matplotlib.pyplot as plt
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
    uinterplation=  (urc1+2.*urc2+2.*urc3+urc4)/6    
    vinterplation= (v1+2.*v2+2.*v3+v4)/6
    #print urc1,v1,urc2,v2,urc3,v3,urc4,v4
    return lon,lat,uinterplation,vinterplation   
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
    return i,min_dist     
def polygonal_barycentric_coordinates(xp,yp,xv,yv):
    N=len(xv)   
    j=np.arange(N)
    ja=(j+1)%N
    jb=(j-1)%N
    Ajab=np.cross(np.array([xv[ja]-xv[j],yv[ja]-yv[j]]).T,np.array([xv[jb]-xv[j],yv[jb]-yv[j]]).T)
    #print "xv:"+str(xv),"yv:"+str(yv)
    Aj=np.cross(np.array([xv[j]-xp,yv[j]-yp]).T,np.array([xv[ja]-xp,yv[ja]-yp]).T)
    Aj=abs(Aj)
    Ajab=abs(Ajab)
    Aj=Aj/max(abs(Aj))
    Ajab=Ajab/max(abs(Ajab))    
    w=xv*0.
    j2=np.arange(N-2)
    for j in range(N):
        w[j]=Ajab[j]*Aj[(j2+j+1)%N].prod()
        #print 'Ajab:'+str(Ajab),'Aj:'+str(Aj)
    w=w/w.sum()
    return w
def VelInterp_lonlat(lonp,latp,Grid,u,v):    
# find the nearest vertex    
    kv,distance=nearlonlat(Grid['lon'],Grid['lat'],lonp,latp)
 #   print kv,lonp,latp
# list of triangles surrounding the vertex kv    
    kfv=Grid['kfv'][0:Grid['nfv'][kv],kv]
  #  print kfv
# coordinates of the (dual mesh) polygon vertices: the centers of triangle faces
    lonv=Grid['lonc'][kfv];latv=Grid['latc'][kfv] 
    w=polygonal_barycentric_coordinates(lonp,latp,lonv,latv)
# baricentric coordinates are invariant wrt coordinate transformation (xy - lonlat), check!    
    #print 'w'+str(w)
# interpolation within polygon, w - normalized weights: w.sum()=1.    
# use precalculated Lame coefficients for the spherical coordinates
# coslatc[kfv] at the polygon vertices
# essentially interpolate u/cos(latitude)
# this is needed for RungeKutta_lonlat: dlon = u/cos(lat)*tau, dlat = vi*tau
    cv=Grid['coslatc'][kfv]
    #print 'cv'+str(cv)    
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
        print times,layer
        return u,v
TIME='2003-01-08 00:00:00' 
numdays=3
latd=43.7
lond=-65.2
depth=0
latsize=[39,45]
lonsize=[-72.,-66]
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
#kf=nearlonlat(lonc,latc,lond,latd) # nearest triangle center F - face

#depthtotal=siglay[:,kv]*h[kv]
#layer=np.argmin(abs(depthtotal-depth))
dt=60*60.
tau=dt/111111.
lont=[]
latt=[]
ufinal=[]
vfinal=[]
for i in range(startrecord,endrecord):
#    u,v=get_uv_web(i,layer=0)
    timeurl='['+str(i)+':1:'+str(i)+']'
#    uvposition=str([layer])+str([kf])
    uvposition=str([0])+'[0:1:90414]'
    url='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?'+'Times'+timeurl+',u'+timeurl+uvposition+','+'v'+timeurl+uvposition
    dataset = open_url(url)
    utotal=np.array(dataset['u'])
    vtotal=np.array(dataset['v'])
    times=np.array(dataset['Times'])
    u=utotal[0,0,:]
    v=vtotal[0,0,:]
################get the point according the position###################
    lont.append(lond)
    latt.append(latd)
    lond,latd,uinterplation,vinterplation=RungeKutta4_lonlat(lond,latd,Grid,u,v,tau)
    print lond,latd,times,uinterplation,vinterplation
    ufinal.append(uinterplation)
    vfinal.append(vinterplation)
    kv,distance=nearlonlat(lon,lat,lond,latd)
    print distance
    if str(distance)=='nan':
        print "now calculate reflecte point"
        print lond,latd,kv,distance
        point_x=lont[-2]
        point_y=latt[-2]
        origin_x=lont[-1]
        origin_y=latt[-1]
        x = point_x - origin_x
        yorz = point_y - origin_y
        newx1 = (x*np.cos(np.radians(90))) - (yorz*np.sin(np.radians(90)))
        newx2 = (x*np.cos(np.radians(270))) - (yorz*np.sin(np.radians(270)))
        newyorz1 = (x*np.sin(np.radians(90))) + (yorz*np.cos(np.radians(90)))
        newyorz2 = (x*np.sin(np.radians(270))) + (yorz*np.cos(np.radians(270)))
        newx1 += origin_x
        newx2 += origin_x
        newyorz1 += origin_y
        newyorz2 += origin_y
        fig=plt.figure(figsize=(7,6))
        plt.plot(point_x,point_y,'bo',origin_x,origin_y,'b+',newx1,newyorz1,'mo',newx2,newyorz2,'mo')
        kv1,distance1=nearlonlat(lon,lat,newx1,newyorz1)
        kv2,distance2=nearlonlat(lon,lat,newx2,newyorz2)
        if distance1<distance2:
            lond=lon[kv1]
            latd=lat[kv1]
        else:
            lond=lon[kv2]
            latd=lat[kv2]
        fig=plt.figure(figsize=(7,6))    
        plt.plot(lon,lat,'r.',lonc,latc,'b+')
        plt.plot(lont,latt,'ro-',lont[-1],latt[-1],'mo',lont[0],latt[0],'mo')
    if distance>0.3:
        break
    
#fig=plt.figure(figsize=(7,6))    
#plt.plot(lon,lat,'r.',lonc,latc,'b+')
#plt.plot(lont,latt,'ro-',lont[-1],latt[-1],'mo',lont[0],latt[0],'mo')
#plt.title('Web model map surface track '+' Time:'+TIME) 
#plt.show()
fig=plt.figure()     
Q=plt.quiver(lont,latt,ufinal,vfinal,scale=5.)  
plt.show() 
'''
rng = pd.date_range(stime, periods=len(ufinal), freq='H')
dfu = pd.DataFrame(ufinal, index=rng,columns=['u'])
dfv=pd.DataFrame(vfinal, index=rng,columns=['v'])
dfu.plot()
dfv.plot()
plt.show()
'''

































