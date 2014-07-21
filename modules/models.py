import sys
import numpy as np
from pydap.client import open_url
import datetime as dt
from matplotlib.dates import num2date, date2num
from matplotlib.ticker import FormatStrFormatter
import matplotlib.mlab as ml
import netCDF4
import scipy
import time
import matplotlib.pyplot as plt
import pandas as pd
# import some local modules
from utilities import nearxy,nearlonlat

def get_dataset(url):
    try:    
        dataset = open_url(url)
           
    except:
        print 'Sorry, ' + url + ' not available.' 
        sys.exit(0)
    return dataset
        
# for 30yr model get the u,v, time,lat_vel,lon_vel
def get_FVCOM(url, dt1):
    dataset = get_dataset(url)
    lat = np.array(dataset['latc'])
    lon = np.array(dataset['lonc'])
    h = np.array(dataset['h'])
    siglay = np.array(dataset['siglay'])           
    jd = np.array(dataset['Times'])
    #convert jd to datetime
    dtime, ids = [], []
    for k in range(len(jd)):
        ymd = jd[k].split('-')
        d = dt.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2][0:2]), int(ymd[2][3:5]), 0, 0)
        #if d > dt1:
        dtime.append(d)
        ids.append(k)
    
    u, v = [], []
    for k in ids:      
        u.append(np.array(dataset['u'][k][0][:]))
        v.append(np.array(dataset['v'][k][0][:]))

    return dtime, lat, lon, u, v, h, siglay

def get_index_latlon(url,lat,lon):
    """calculate the index of lat and lon"""
    dataset = get_dataset(url)
    basemap_lat = dataset['lat']
    basemap_lon = dataset['lon']
    basemap_topo = dataset['topo']
    # add the detail of basemap
    index_lat = int(round(np.interp(lat, basemap_lat, range(0, basemap_lat.shape[0]))))
    index_lon = int(round(np.interp(lon, basemap_lon, range(0, basemap_lon.shape[0]))))
    return index_lat, index_lon, basemap_topo

def getdepth(lat, lon):
    """
    get the USGS depth for lat,lon
    """
    url = 'http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v1_0'
    index_lat, index_lon, basemap_topo = get_index_latlon(url,lat,lon)
    if index_lat == 0 or index_lon == 0:        
        url = 'http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc'
        index_lat, index_lon, basemap_topo = get_index_latlon(url,lat,lon)
    return basemap_topo.topo[index_lat, index_lon]

def getFVCOM_bottom_temp(url, time0, mlon, mlat):
    """get depth from the getmodel"""
    dataset = get_dataset(url)
    tri = dataset['nv'] 
    jdmat_m = list(dataset['Times'])
    temp = dataset['temp']
    h_vel = list(dataset['h'])
    siglay = dataset['siglay']
    lat_vel = list(dataset['lat'])
    lon_vel = list(dataset['lon'])
      
    # get the tri0,tri1,tri2 as the location of three points
    tri0 = [i for i in tri[0]]
    tri1 = [i for i in tri[1]]
    tri2 = [i for i in tri[2]]
        
    lat_vel_1, lon_vel_1 = [], []
    for i in range(len(tri0)):
        if tri1[i] == len(lat_vel):
            tri1[i] = len(lat_vel) - 1
        if tri2[i] == len(lat_vel):
            tri2[i] = len(lat_vel) - 1
        lat_vel_1.append(float((lat_vel[tri0[i]] + lat_vel[tri1[i]] + lat_vel[tri2[i]])) / float(3))
        lon_vel_1.append(float((lon_vel[tri0[i]] + lon_vel[tri1[i]] + lon_vel[tri2[i]])) / float(3))
    # get the min distance
    (distance, index_location) = nearxy(lon_vel_1, lat_vel_1, mlon, mlat)
    (disth, index_location_h) = nearxy(lon_vel, lat_vel, mlon, mlat)
        
    #exclude incorrect data
    jdmat = [jd for jd in jdmat_m if jd[17:19] != 60]  

    jdmat_m_num = [] # this is the data in the form of a number
    for i in jdmat:  
        jdmat_m_num.append(date2num(dt.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%f')))
  
    depths = h_vel[index_location_h] * siglay[:, index_location_h]

    #get the ids of depths
    depths_list = []
    for d in range(0, len(depths)):
        depths_list.append(depths[d])
    depths_list.reverse() #Where is this used???
    
    jdmat_index = range(len(jdmat_m_num))
    index_time = int(round(np.interp(time0, jdmat_m_num, jdmat_index)))
    temperature = list(temp[index_time, :, index_location_h])
            
    return depths, temperature


def getFVCOM_depth(lati,loni):#vname='temp'or'salinity'
        '''
        Function written by Jim Manning
        generates model depth data as a DataFrame
        '''
        urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
        nc = netCDF4.Dataset(urlfvcom)
        nc.variables
        lat = nc.variables['lat'][:]
        lon = nc.variables['lon'][:]
        dep = nc.variables['h'][:]
        inode = nearlonlat(lon,lat,loni,lati)
        return dep[inode]            

def getFVCOM_bottom_tempsalt_netcdf(lati,loni,starttime,endtime,layer,vname):#vname='temp'or'salinity'
        '''
        Function written by Yacheng Wang
        generates model data as a DataFrame
        according to time and local position
        different from getFVCOM_bottom_temp:
        this function only return time-temp dataframe and ues netcdf4
        getFVCOM_bottom_temp return depth and temp
        '''
        urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
        nc = netCDF4.Dataset(urlfvcom)
        nc.variables
        lat = nc.variables['lat'][:]
        lon = nc.variables['lon'][:]
        times = nc.variables['time']
        jd = netCDF4.num2date(times[:],times.units)
        var = nc.variables[vname]
        inode = nearlonlat(lon,lat,loni,lati)
        modindex=netCDF4.date2index([starttime,endtime],times,select='nearest')
        modtso=pd.DataFrame(var[modindex[0]:modindex[1],layer,inode],index=jd[modindex[0]:modindex[1]])
        return modtso
        
def getmodel_GOMPOM(mlat, mlon, depth_i, stime, etime, dataset):
    "use this function to get 'GOMPOM'"
    U_array = dataset['u']
    V_array = dataset['v']
    time_array = dataset['time_run']
    time_hour = dataset['time']
    lon_array = dataset['xpos']
    lat_array = dataset['ypos']
    depths_sigma = dataset['depth_at_sigma']
    depth = dataset['depth']
    #change all arrays to lists
    time = []
    lon = [(i - 360) for i in lon_array]
    lat = [i for i in lat_array]
    time_hour_list = [i for i in time_hour]

    time_num = date2num(dt.datetime.strptime(str(time_array[0]), '%Y-%m-%dT%H:%M:%SZ'))

    for i in time_hour_list:
        time.append(float(i / 24) + time_num - 1)
    print stime, time[0]
     
    lat_min = [(abs(i - mlat)) for i in lat]
    lon_min = [(abs(i - mlon)) for i in lon]
    for i in range(len(lat_min)):
        if lat_min[i] == min(lat_min):
            index_lat = i
    for i in range(len(lon_min)):
        if lon_min[i] == min(lon_min):
            index_lon = i

    depths = depth[index_lat, index_lon].data[0] * depths_sigma[:, index_lat, index_lon].data[1] 
    depths_list = [i for i in depths]
    index_list = [i for i in range(len(depths_list))]
    depths_list.reverse()
    index_list.reverse()
    idz = int(round(np.interp(depth_i, depths_list, index_list)))
    # get u&v
    u_array = U_array.u[:, idz, index_lat, index_lon]
    v_array = V_array.v[:, idz, index_lat, index_lon]
    u_list = [i for i in u_array]
    v_list = [i for i in v_array]
    part_time, part_u, part_v = [], [], []
    u = None
    print time[0], time[len(time) - 1]
    for i in range(len(time)):
        if stime <= time[i] <= etime:
            part_time.append(time[i])
            part_v.append(v_list[i])
            part_u.append(u_list[i])
    return part_time, part_u, part_v, u

# model of 30yr & MASSBAY
def getmodel_step1(url, model):
    """
    step1 of getmodel or GOMPOM.
    choose model first,then get data from the url
    """
    dataset = get_dataset(url)
        
    if model != "GOMPOM":
        # all models EXCEPT GOMPOM
        jdmat_m = dataset['Times']
        ms = str(jdmat_m[0])  #forming a string of the model start time
        me = str(jdmat_m[-1])
        modsdate = dt.datetime.strptime(ms[0:-7], '%Y-%m-%dT%H:%M:%S')
        modedate = dt.datetime.strptime(me[0:-7], '%Y-%m-%dT%H:%M:%S')
    else:
        # special case of GOMPOM model
        time_array = dataset['time_run'] 
        time_hour = dataset['time']
        time_hour_list = [i for i in time_hour]
        time_num = date2num(dt.datetime.strptime(str(time_array[0]), '%Y-%m-%dT%H:%M:%SZ'))
        timet = [(float(i / 24) + time_num - 1) for i in time_hour_list]
      
        modsdate = num2date(timet[0]) 
        modedate = num2date(timet[-1])
    print "The start time and end you input should be between " + str(modsdate) + " and " + str(modedate)
    mlat = 40.956
    mlon = -67.626   
    depth_i = -.5
    stime1 = '1995,3,20,00:00:00'
    etime1 = '1995,3,25,00:00:00';
    #mlat=float(raw_input("please input the latitide: "))
    #mlon=float(raw_input("please input the longitude: "))
    #depth_i=float(raw_input("please input the depth(example:-2): "))
    #stime1=raw_input("please input the start date(example:2012,3,2,23:59:59): ")
    #etime1=raw_input("please input the end date(example:2012,3,2,23:59:59): ")
    stime = date2num(dt.datetime.strptime(stime1, '%Y,%m,%d,%H:%M:%S'))
    etime = date2num(dt.datetime.strptime(etime1, '%Y,%m,%d,%H:%M:%S'))

    #find the index of desired time
    print 'finding index for desired time'
    ids = ml.find(np.array(jdmat_m) == stime) 
    ide = ml.find(np.array(jdmat_m) == etime)
    return mlat, mlon, depth_i, stime, etime, dataset, modsdate, modedate, ids, ide
      

def getmodel(stime, etime, mlon, mlat, depth_i, modsdate, modedate, dataset): # after getmodel_GOMPOM_step1 
  
    tri = dataset['nv'] 
    jdmat_m = dataset['Times']
    while (stime < date2num(modsdate))  or (etime > date2num(modedate)):
        print "sorry no model data available for that time"
        sys.exit(0)
    u = dataset['u']
    v = dataset['v']
    # zeta=dataset['zeta']
    h = dataset['h']
    siglay = dataset['siglay']
    lat_array = dataset['lat']
    lon_array = dataset['lon']
    #get the lat & lon
    lat_vel = [i for i in lat_array]
    lon_vel = [i for i in lon_array]
    # get the tri0,tri1,tri2 as the location of three points
    tri0 = [i for i in tri[0]]
    tri1 = [i for i in tri[1]]
    tri2 = [i for i in tri[2]]
 
    h_vel = [h_i for h_i in h]
  
    lat_vel_1, lon_vel_1 = [], []
    for i in range(len(tri0)):
        if tri1[i] == len(lat_vel):
            tri1[i] = len(lat_vel) - 1
        if tri2[i] == len(lat_vel):
            tri2[i] = len(lat_vel) - 1
        lat_vel_1.append(float((lat_vel[tri0[i]] + lat_vel[tri1[i]] + lat_vel[tri2[i]])) / float(3))
        lon_vel_1.append(float((lon_vel[tri0[i]] + lon_vel[tri1[i]] + lon_vel[tri2[i]])) / float(3))
  # get the min distance
  # if url=='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3':
  #    (distance,index_location) = nearxy(lon_vel,lat_vel,mlon,mlat)
  #else:
    print 'finding index of this location'    
    (distance, index_location) = nearxy(lon_vel_1, lat_vel_1, mlon, mlat)
    (disth, index_location_h) = nearxy(lon_vel, lat_vel, mlon, mlat)

    print 'making list of jdmat'
    jdmat_m_list = list(jdmat_m)
    print 'removing the bad data from jdmat'
    del_list, jdmat, del_index = [], [], []
    for i in range(len(jdmat_m_list)):
        if jdmat_m_list[i][17:19] == '60':  #delete the wrong data
            del_list.append(jdmat_m_list[i])
            del_index.append(i)
    jdmat = [val for val in jdmat_m_list if val not in del_list]
    jdmat_m_num = []                    # this is the data in the form of a number
    print 'reformatting jdmat using strptime'
    for i in jdmat:  
        jdmat_m_num.append(date2num(dt.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%f')))

    depths = h_vel[index_location_h] * siglay[:, index_location_h]
    print 'found the depths of the model at this location'
  
    #get the ids of depths
    depths_list = [depths[id] for id in range(0, len(depths))]
    depths_list.reverse()
    ids = range(len(depths_list))
    ids.reverse()
    idz = int(round(np.interp(depth_i, depths_list, ids)))
 
    print 'finding index of this date'
    index_sdate = int(round(np.interp(stime, jdmat_m_num, range(len(jdmat_m_num)))))
    index_edate = int(round(np.interp(etime, jdmat_m_num, range(len(jdmat_m_num)))))
  
    del_index_idz = [i for i in range(len(del_index))]
  
    if del_index_idz:   
        index_u_sdate = int(np.ceil(np.interp(index_sdate, del_index, del_index_idz)))
        index_u_edate = int(np.ceil(np.interp(index_edate, del_index, del_index_idz)))
    else:
        index_u_sdate = 0
        index_u_edate = 0

    index_sdate1 = index_u_sdate + index_sdate
    index_edate1 = index_u_edate + index_edate
    v_part = v[index_sdate1:index_edate1, idz, index_location]
    u_part = u[index_sdate1:index_edate1, idz, index_location]
    time1 = num2date(jdmat_m_num[index_sdate:index_edate])  

    del_index.reverse()  
  
    v_list = [i for i in v_part]
    u_list = [i for i in u_part]
  
    #beginning of each month time is same, so delete
    del_index_time = []
    for i in range(1, len(time1)):
        if time1[i - 1] == time1[i]:
            del_index_time.append(i)
    if del_index_time:
        del u_list[del_index_time[0]]
        del v_list[del_index_time[0]]
        del time1[del_index_time[0]]
    print 'done getmodel function'
    return time1, u_list, v_list, lat_vel, lon_vel


def get_ncep_winds(lat1, lon1, year):
    """
    get the wind from url
    """
    url_v = 'http://www.cdc.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/surface/vwnd.sig995.'
    url_u = 'http://www.cdc.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/surface/uwnd.sig995.'
    dataset1 = open_url(url_v + str(year) + '.nc?vwnd')
    dataset2 = open_url(url_u + str(year) + '.nc?uwnd')
    vwnd = dataset1['vwnd']
    uwnd = dataset2['uwnd']  
    #get lat list
    lat_i = list(scipy.arange(len(vwnd.lat[0:])))
    lat_i.reverse()
    lat = list(vwnd.lat[0:])
    lat.reverse()
    #get lon list
    lon = list(vwnd.lon[0:] - 360)
    lon_i = list(scipy.arange(len(vwnd.lon[0:])))

    #get id of lat1,lon1
    idlat = int(round(np.interp(lat1, lat, lat_i)))
    idlon = int(round(np.interp(lon1, lon, lon_i)))
    #get uw,vw
    grid_v = vwnd[0:len(vwnd.time[0:]), idlat, idlon]
    grid_u = uwnd[0:len(vwnd.time[0:]), idlat, idlon]
    uw = np.squeeze(grid_u.array) * 0.01 + 225.45
    vw = np.squeeze(grid_v.array) * 0.01 + 225.45
    #get time
    jdmat_w = uwnd.time[0:] / 24
    uw = list(uw)
    vw = list(vw)
    jdmat_w = list(jdmat_w)

    del_another_year = []
    for i in range(len(jdmat_w)):
        if num2date(jdmat_w[i]).year > num2date(jdmat_w[0]).year:
            del_another_year.append(i)
    del_another_year.reverse()
    for i in del_another_year:
        del jdmat_w[i]
        del uw[i]
        del vw[i]
  
    return uw, vw, jdmat_w

def getroms(url):
    """
    returns all the velocity fields
    """
    dataset = get_dataset(url)
    jdmat_2, jdmat_m, u2, v2, u, v = [], [], [], [], [], []
    jdmat_1 = dataset['ocean_time'] #ocean_time is in seconds from 2006-01-01 where dstart is in days
    for i in jdmat_1:
        time_tuple = time.gmtime(i + 1016884800.0)#convert second to datetime     
        yr = time_tuple.tm_year
        mth = time_tuple.tm_mon
        day = time_tuple.tm_mday
        hr = time_tuple.tm_hour
        mn = time_tuple.tm_min
        se = time_tuple.tm_sec
        jdmat_2.append(date2num(dt.datetime(yr, mth, day, hr, mn, se)))      
      
    print "The roms model start date is ", num2date(jdmat_2[0]), "end date is ", num2date(jdmat_2[-1])
    print "\nInside the getroms function we have"
    print "jdmat_2[0],(jdmat_2[-1]-jdmat_2[0])/24,shape(jdmat_2) as:"
    print jdmat_2[0], (jdmat_2[-1] - jdmat_2[0]) / 24, np.shape(jdmat_2)
    lat_u = list(dataset['lat_u'])
    lon_u = list(dataset['lon_u'])
    lat_v = list(dataset['lat_v'])
    lon_v = list(dataset['lon_v'])
    u1 = dataset['u']
    v1 = dataset['v']
    
    lon_u = np.array(lon_u) # why do I change it back to array here????
    lat_u = np.array(lat_u)
    lon_v = np.array(lon_v)
    lat_v = np.array(lat_v)
    lon_u = lon_u.reshape(np.size(lon_u))
    lat_u = lat_u.reshape(np.size(lat_u))
    lon_v = lon_v.reshape(np.size(lon_v))
    lat_v = lat_v.reshape(np.size(lat_v))
    
    u = u1[:, 0, :, :] # here I am asking for the surface value so index_z=0
    v = v1[:, 0, :, :]
    return jdmat_2, lat_u, lon_u, lat_v, lon_v, u, v
    

def gettrack_FVCOM(depth, jdmat_m, lat_vel_1, lon_vel_1, u, v, lat_vel, lon_vel, h_vel, siglay, startdate, numdays, daystep, la, lo):
    """get the track for models"""

    # calculate the points near la,la
    (disth, index_location_h) = nearxy(lon_vel, lat_vel, lo, la)
    (distance, index_location) = nearxy(lon_vel_1, lat_vel_1, lo, la)
    # calculate all the depths
    depths = h_vel[index_location_h] * siglay[:, index_location_h]
    # make depths to be descending order
    new_depths = list(depths).reverse()
    # depths range
    range_depths = range(len(depths)).reverse()            
    # calculate the index of depth in the depths            
    idz = int(round(np.interp(depth, new_depths, range_depths)))
    print "the depth index is:", idz
    ####### get index of startdate in jdmat_m#####
    jdmat_m_num = [] # this is the data in the form of a number
    del_list, jdmat, del_index = [], [], []
    # convert array to list
    jdmat_m_list = [jdmat_m_i for jdmat_m_i in jdmat_m]
    # while seconds=60, can change the datetime to number, so delete
          
    for i in range(1, len(jdmat_m_list)):
        if jdmat_m_list[i][17:19] == '60' or jdmat_m_list[i - 1] == jdmat_m_list[i]:          
            del_list.append(jdmat_m_list[i])
            del_index.append(i)                              #get the index of deleted datetime
    jdmat = [val for val in jdmat_m_list if val not in del_list]# delete the wrong value, jdmat just 
    for i in jdmat:  # convert time to number
        jdmat_m_num.append(date2num(dt.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%f')))
            
    index_startdate_1 = int(round(np.interp(date2num(startdate), jdmat_m_num, range(len(jdmat_m_num)))))#get the index of startdate
    print "the index of start date is:", index_startdate_1 
    # calculate the delete index of time for u and v
   
    if del_index != []:
        index_add = int(np.ceil(np.interp(index_startdate_1, del_index, range(len(del_index)))))
        index_startdate = index_add + index_startdate_1
    else:
        index_startdate = index_startdate_1

    # get u,v
    u1 = float(u[index_startdate, idz, index_location])
    v1 = float(v[index_startdate, idz, index_location])

    nsteps = scipy.floor(min(numdays, jdmat_m_num[-1]) / daystep)
    # get the velocity data at this first time & place
    lat_k = 'lat' + str(1)
    lon_k = 'lon' + str(1)
    uu, vv, lon_k, lat_k, time = [], [], [], [], []
    uu.append(u1)
    vv.append(v1)
    lat_k.append(la)
    lon_k.append(lo)
    time.append(date2num(startdate))
    delete_id = [] 

    for i in range(1, int(nsteps)):
        # first, estimate the particle move to its new position using velocity of previous time steps
        
        lat1 = lat_k[i - 1] + vv[i - 1] * daystep * 0.7769085
        lon1 = lon_k[i - 1] + uu[i - 1] * daystep * 0.7769085 * scipy.cos(lat_k[i - 1] / 180 * np.pi)
        # find the closest model time for the new timestep
        jdmat_m_num_i = time[i - 1] + daystep
        time.append(jdmat_m_num_i)

        index_startdate_1 = int(round(np.interp(jdmat_m_num_i, jdmat_m_num, range(len(jdmat_m_num)))))
        if del_index != []:
            index_add = int(np.ceil(np.interp(index_startdate_1, del_index, range(len(del_index)))))
            index_startdate = index_add + index_startdate_1
        else:
            index_startdate = index_startdate_1
        #find the point's index of near lat1,lon1
        index_location = nearxy(lon_vel_1, lat_vel_1, lon1, lat1)[1]
        # calculate the model depth
        depth_model = getdepth(lat_k[i - 1], lon_k[i - 1])
        #get u and v
        ui = u[index_startdate, idz, index_location]
        vi = v[index_startdate, idz, index_location]
        vv.append(vi)
        uu.append(ui)
        # estimate the particle move from its new position using velocity of previous time steps   
        
        lat_k.append((lat1 + lat_k[i - 1] + vv[i] * daystep * 0.7769085) / 2.)
        lon_k.append((lon1 + lon_k[i - 1] + uu[i] * daystep * 0.7769085 * scipy.cos(lat_k[i] / 180 * np.pi)) / 2.)
        
    if depth_model > 0:
        delete_id.append(i)
        #delete the depth is greater than 0
        delete_id.reverse()
        for i in delete_id:
            del lat_k[i]
            del lon_k[i]
            del time[i]
            del uu[i]
            del vv[i]
        if delete_id != []:
            del lat_k[-1]
            del lon_k[-1]
            del time[-1]
            del uu[-1]
            del vv[-1]
        return lat_k, lon_k, time, uu, vv


def gettrack_raw(numdays, startdate, driftid, data_file):
    #startdate is a datetime
    yeardays_start = date2num(dt.datetime(1, startdate.month, startdate.day))
    ye = num2date(date2num(startdate) + numdays)
    yeardays_end = date2num(dt.datetime(1, ye.month, ye.day))
    verts = []
    f = open(data_file, 'r')
    for line in f:
        verts.append(line)
    
    lat, lon, yearday = [], [], []   

    for vert in verts:
        if vert.split()[0] == driftid and str(yeardays_start - 1) <= vert.split()[6] <= str(yeardays_end - 1):
            lat.append(vert.split()[8])
            lon.append(vert.split()[7])
            yearday.append(vert.split()[6])
    yearday_raw = [float(i) + 1 for i in yearday]
    lat = [float(i) for i in lat]
    lon = [float(i) for i in lon]
    return lat, lon, yearday_raw

def gettrack_roms(jdmat_m, lon_v, lat_v, u, v, startdate, numdays, daystep, la, lo): # tracks particle at surface
    # calculate the points near la,lo
    distance, index_location = nearxy(lon_v, lat_v, lo, la)
    ####### get index of startdate in jdmat_m#####
    jdmat_m_num = [] # this is the date in the form of a number
    jdmat_m_list, jdmat = [], []
    # convert array to list
    for jdmat_m_i in jdmat_m:
        jdmat_m_list.append(jdmat_m_i)
    for i in jdmat_m_list:  # convert time to number
        jdmat_m_num.append(i)
    dts = date2num(dt.datetime(2001, 1, 1, 0, 0, 0))
    jdmat_m = [i + dts for i in jdmat_m]
    index_startdate = int(round(np.interp(startdate, jdmat_m, range(len(jdmat_m)))))#get the index of startdate
    print "index_startdate = ", index_startdate, " inside getreack_roms  "          
    print "the start u's location", index_location
    u1 = float(u[index_startdate][index_location])
    v1 = float(v[index_startdate][index_location])
    if u1 == -999.0:  # case of no good data
        u1 = 0
        v1 = 0
    
    nsteps = scipy.floor(min(numdays, jdmat_m_num[-1]) / daystep)
    print "nsteps =", nsteps
    
    uu, vv, lon_k, lat_k, time = [], [], [], [], []
    uu.append(u1)
    vv.append(v1)
    lat_k.append(la)
    lon_k.append(lo)
    time.append(startdate)
              
    for i in range(1, int(nsteps)):
        # first, estimate the particle move to its new position using velocity of previous time steps
        lat1 = lat_k[i - 1] + float(vv[i - 1] * daystep * 24 * 3600) / 1000 / 1.8535 / 60
        lon1 = lon_k[i - 1] + float(uu[i - 1] * daystep * 24 * 3600) / 1000 / 1.8535 / 60 * (scipy.cos(float(lat_k[i - 1])) / 180 * np.pi)
        # find the closest model time for the new timestep
        jdmat_m_num_i = time[i - 1] + daystep
        time.append(jdmat_m_num_i)
        if jdmat_m_num_i > max(jdmat_m_num):
            print "This time is not available in the model"
        index_startdate = int(round(np.interp(jdmat_m_num_i, jdmat_m_num, range(len(jdmat_m_num)))))
               
        #find the point's index of near lat1,lon1
        index_location = nearxy(lon_v, lat_v, lon1, lat1)[1]
         
        ui = u[index_startdate][index_location]
        vi = v[index_startdate][index_location]
                
        vv.append(vi)
        uu.append(ui)
        # estimate the particle move from its new position using velocity of previous time steps
        lat_k.append(float(lat1 + lat_k[i - 1] + float(vv[i] * daystep * 24 * 3600) / 1000 / 1.8535 / 60) / 2)
        lon_k.append(float(lon1 + lon_k[i - 1] + float(uu[i] * daystep * 24 * 3600) / 1000 / 1.8535 / 60 * scipy.cos(float(lat_k[i]) / 180 * np.pi)) / 2)
             
    return lat_k, lon_k, time
    
def model_plot_track(depth, jdmat_m, lat_vel_1, lon_vel_1, u, v, lat_vel, lon_vel, h_vel, siglay, startdate, numdays, daystep, x, la, lo):
    fig = plt.figure(1)
    if len(depth) == 1:
        panels = len(startdate)
    if len(depth) != 1:
        panels = len(depth)
    for j in range(1, panels + 1):
        print int(str(panels) + str(2) + str(j))
        if panels == 1:
            ax = fig.add_subplot(111)
        else:
            ax = fig.add_subplot(int(str(2) + str(2) + str(j)))
        if j == 3:
            plt.xlabel('Longitude W')
        if j == 1:
            plt.ylabel('Latitude N')
        for k in range(len(la)):
            for m in range(len(lo)):            
                (distance, index_location) = nearxy(lon_vel_1, lat_vel_1, lo[m], la[k])
                (disth, index_location_h) = nearxy(lon_vel, lat_vel, lo[m], la[k])
            
                depths = h_vel[index_location_h] * siglay[:, index_location_h]
                # make depths to be descending order
                new_depths = list(depths)
                new_depths.reverse()
                # depths range
                range_depths = range(len(depths))
                range_depths.reverse()
                if len(depth) == 1:
                    idz = 0
                else:
                    idz = int(round(np.interp(depth[j - 1], new_depths, range_depths)))
            
                ####### get index of startdate in jdmat_m
                jdmat_m_num = [] # this is the data in the form of a number
                del_list, jdmat, del_index = [], [], []
                # convert array to list
                jdmat_m_list = [jdmat_m_i for jdmat_m_i in jdmat_m]
           
                # while seconds=60, can change the datetime to number, so delete
                for i in range(1, len(jdmat_m_list)):
                    if jdmat_m_list[i][17:19] == '60' or jdmat_m_list[i - 1] == jdmat_m_list[i]:                  
                        del_list.append(jdmat_m_list[i])
                        del_index.append(i)#get the index of deleted datetime
                jdmat = [val for val in jdmat_m_list if val not in del_list] # delete the wrong value, jdmat just 
                for i in jdmat:  # convert time to number
                    jdmat_m_num.append(date2num(dt.datetime.strptime(i, '%Y-%m-%dT%H:%M:%S.%f')))
                # get index of startdate in jdmat_m_num
                index_startdate_1 = int(round(np.interp(date2num(startdate[j - 1]), jdmat_m_num, range(len(jdmat_m_num)))))
                if del_index != []:
                    index_add = int(np.ceil(np.interp(index_startdate_1, del_index, range(len(del_index)))))
                    index_startdate = index_add + index_startdate_1
                else:
                    index_startdate = index_startdate_1
                # get u,v
                u1 = float(u[index_startdate, idz, index_location])
                v1 = float(v[index_startdate, idz, index_location])
                nsteps = scipy.floor(min(numdays, jdmat_m_num[-1]) / daystep)
                # get the velocity data at this first time & place
                lat_k = 'lat' + str(k)
                lon_k = 'lon' + str(k)
                uu, vv, lon_k, lat_k, time = [], [], [], [], []
                uu.append(u1)
                vv.append(v1)
                lat_k.append(la[k])
                lon_k.append(lo[m])
                time.append(date2num(startdate[j - 1]))
    
            
            for i in range(1, int(nsteps)):
                # first, estimate the particle move to its new position using velocity of previous time steps
                lat1 = lat_k[i - 1] + float(vv[i - 1] * daystep * 24 * 3600) / 1000 / 1.8535 / 60
                lon1 = lon_k[i - 1] + float(uu[i - 1] * daystep * 24 * 3600) / 1000 / 1.8535 / 60 * (scipy.cos(float(lat_k[i - 1])) / 180 * np.pi)
                # find the closest model time for the new timestep
                jdmat_m_num_i = time[i - 1] + daystep
                time.append(jdmat_m_num_i)

                index_startdate_1 = int(round(np.interp(jdmat_m_num_i, jdmat_m_num, range(len(jdmat_m_num)))))
                if del_index != []:                    
                    index_add = int(np.ceil(np.interp(index_startdate_1, del_index, range(len(del_index)))))
                    index_startdate = index_add + index_startdate_1
                else:
                    index_startdate = index_startdate_1
                #find the point's index of near lat1,lon1
                index_location = nearxy(lon_vel_1, lat_vel_1, lon1, lat1)[1]
                ui = u[index_startdate, 1, index_location]
                vi = v[index_startdate, 1, index_location]
                vv.append(vi)
                uu.append(ui)
                # estimate the particle move from its new position using velocity of previous time steps
                lat_k.append(float(lat1 + lat_k[i - 1] + float(vv[i] * daystep * 24 * 3600) / 1000 / 1.8535 / 60) / 2)
                lon_k.append(float(lon1 + lon_k[i - 1] + float(uu[i] * daystep * 24 * 3600) / 1000 / 1.8535 / 60 * scipy.cos(float(lat_k[i]) / 180 * np.pi)) / 2)
              
            plt.plot(lon_k, lat_k, "-", linewidth=1, marker=".", markerfacecolor='r')
            basemap([min(lat_k) - 2, max(lat_k) + 2], [min(lon_k) - 2, max(lon_k) + 2])
            # make same size for the panels
            min_lat, max_lon, max_lat, min_lon = [], [], [], []
            min_lat.append(min(lat_k))
            max_lat.append(max(lat_k))
            min_lon.append(min(lon_k))
            max_lon.append(max(lon_k))
            
            text1 = ax.annotate(str(num2date(time[0]).month) + "-" + str(num2date(time[0]).day),
                                xy=(lon_k[0], lat_k[0]),
                                xycoords='data',
                                xytext=(8, 10),
                                textcoords='offset points',
                                arrowprops=dict(arrowstyle="->"))
            text1.draggable()
            text1 = ax.annotate(str(num2date(time[-1]).month) + "-" + str(num2date(time[-1]).day),
                                xy=(lon_k[-1], lat_k[-1]),
                                xycoords='data',
                                xytext=(8, 10),
                                textcoords='offset points',
                                arrowprops=dict(arrowstyle="->"))


        #set the numbers formatter
        majorFormatter = FormatStrFormatter('%.2f')
        ax.yaxis.set_major_formatter(majorFormatter)
        ax.xaxis.set_major_formatter(majorFormatter)
        if len(depth) == 1:
            plt.title(str(num2date(time[i - 1]).year))
        else:
            plt.title(str(num2date(time[i - 1]).year) + " year" + " depth: " + str(depth[j - 1]))
        
        ax.xaxis.set_label_coords(0.5, -0.005)   #set the position of the xlabel
        ax.yaxis.set_label_coords(-0.1, 0.5)
        plt.xlim([min(min_lon), max(max_lon)])
        plt.ylim([min(min_lat), max(max_lat)])
    plt.show()
