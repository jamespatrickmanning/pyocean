import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import num2date,date2num
import datetime
import scipy
from utilities import nearxy
import math
from basemap import basemap_usgs

def gettrack_codar(jdmat_m,lon_vel,lat_vel,u,v,startdate,numdays,daystep,la,lo):
    """
    tracks particle at surface
    """
    # calculate the points near la,la
    distance,index_location=nearxy(lon_vel,lat_vel,lo,la)
    
    ####### get index of startdate in jdmat_m#####
    jdmat_m_num=[] # this is the date in the form of a number
    jdmat_m_list,jdmat=[],[]
    # convert array to list
    for jdmat_m_i in jdmat_m:
        jdmat_m_list.append(jdmat_m_i)
    for i in jdmat_m_list:  # convert time to number
        jdmat_m_num.append(i)
    dts=date2num(datetime.datetime(2001,1,1,0,0,0))
    jdmat_m=[i+dts for i in jdmat_m]
    index_startdate=int(round(np.interp(startdate,jdmat_m,range(len(jdmat_m)))))#get the index of startdate
    # get u,v
    u1=float(u[index_startdate][index_location])
    v1=float(v[index_startdate][index_location])
    if u1==-999.0/100:# case of no good data
        u1=0
        v1=0
    nsteps=scipy.floor(min(numdays,jdmat_m_num[-1])/daystep)
    # get the velocity data at this first time & place
    lat_k='lat'+str(1)
    lon_k='lon'+str(1)
    uu,vv,lon_k,lat_k,time=[],[],[],[],[]
    uu.append(u1)
    vv.append(v1)
    lat_k.append(la)
    lon_k.append(lo)
    time.append(startdate)
              
    for i in range(1,int(nsteps)):
        # first, estimate the particle move to its new position using velocity of previous time steps
        lat1=lat_k[i-1]+float(vv[i-1]*daystep*24*3600)/1000/1.8535/60
        lon1=lon_k[i-1]+float(uu[i-1]*daystep*24*3600)/1000/1.8535/60*(scipy.cos(float(lat_k[i-1]))/180*np.pi)
        # find the closest model time for the new timestep
        jdmat_m_num_i=time[i-1]+daystep
        time.append(jdmat_m_num_i)
        #print jdmat_m_num_i

        index_startdate=int(round(np.interp(jdmat_m_num_i,jdmat_m_num,range(len(jdmat_m_num)))))
        #find the point's index of near lat1,lon1
        index_location=nearxy(lon_vel,lat_vel,lon1,lat1)[1]
        ui=u[index_startdate][index_location]
        vi=v[index_startdate][index_location]
        #if u1<>-999.0/100:# case of good data
        vv.append(vi)
        uu.append(ui)
        # estimate the particle move from its new position using velocity of previous time steps
        lat_k.append(float(lat1+lat_k[i-1]+float(vv[i]*daystep*24*3600)/1000/1.8535/60)/2)
        lon_k.append(float(lon1+lon_k[i-1]+float(uu[i]*daystep*24*3600)/1000/1.8535/60*scipy.cos(float(lat_k[i])/180*np.pi))/2)
        #else:
        #  vv.append(0)
        #  uu.append(0)
          # estimate the particle move from its new position using velocity of previous time steps
        #  lat_k.append(float(lat1))
        #  lon_k.append(float(lon1))      
    return lat_k,lon_k,time

def progvec(time,u,v): #time is number 
    tintv=np.diff(time)*24*3600
    mag,x_model,y_model=[],[],[]
    x_model.append(0.0)
    y_model.append(0.0)
    mag.append(0.0)
    for i in range(1,len(tintv)):
        tx=(tintv[i-1]*float(u[i-1]+u[i]))/2/1000
        # THE FOLLOWING PRINT WARNING WILL OCCUR FOR >200 CM/S
        if abs(tx)>200:
            print num2date(time[i]),time[i]
        ty=tintv[i-1]*float(v[i-1]+v[i])/2/1000
        tmag=np.sqrt(tx**2+ty**2)
        x_model.append(x_model[i-1]+tx)
        y_model.append(y_model[i-1]+ty)
        mag.append(mag[0]+tmag)
    np.save('fcast.time',time)    
    return x_model,y_model
    


def progvec_plot(x_model,y_model,mlat,mlon,depth_i,stime1,etime1):
    
    fig = plt.figure()
    fig.canvas.set_window_title('progvec')
    ax1 = fig.add_subplot(111)
    ax1.plot(x_model,y_model,"-")
    plt.xlabel('km')
    plt.ylabel('km')
    plt.title('The time from '+str(stime1)+' to '+str(etime1)
    +'\n'+'latitude:'+str(mlat)+' longitude:'+str(mlon)+' depth:'+str(depth_i))

    plt.figure() 
    lo,la=[],[]
    for k in range(len(x_model)):
        lo.append(mlon+x_model[k]/1.86/60/math.cos(mlat/180.*math.pi))
        la.append(mlat+y_model[k]/1.86/60)
    basemap_usgs(la,lo,True)    
    plt.plot(lo,la,'-')
    np.save('fcast.lat',la)
    np.save('fcast.lon',lo)
   
    plt.show()
