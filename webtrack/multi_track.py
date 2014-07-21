
# multi_track

'''
GENERAL NOTES:
    1. Initializations need to be at the beginning of the program or function
    2. Needs more spacing and notes
    3. If any changes are made, the flowcharts MUST be updated
            
'''

'''Import modules'''

import sys
sys.path.append('../moj')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import jata
from datetime import datetime, timedelta
from matplotlib import path
from conversions import dm2dd,distance
from getdata import getdrift,getrawdrift
import calendar
import pytz
sys.path.append('../bin')
import netCDF4 

class track(object):
    def __init__(self, startpoint):
        '''
        gets the start point of the water, and the location of datafile.
        '''
        self.startpoint = startpoint
        
    def get_data(self, url):
        '''
        calls get_data
        '''        
        pass                                 
        
    def bbox2ij(self, lons, lats, bbox):
        """
        Return tuple of indices of points that are completely covered by the 
        specific boundary box.
        i = bbox2ij(lon,lat,bbox)
        lons,lats = 2D arrays (list) that are the target of the subset, type: np.ndarray
        bbox = list containing the bounding box: [lon_min, lon_max, lat_min, lat_max]
    
        Example
        -------  
        >>> i0,i1,j0,j1 = bbox2ij(lat_rho,lon_rho,[-71, -63., 39., 46])
        >>> h_subset = nc.variables['h'][j0:j1,i0:i1]       
        """
        
        bbox = np.array(bbox)
        mypath = np.array([bbox[[0,1,1,0]],bbox[[2,2,3,3]]]).T
        p = path.Path(mypath)
        points = np.vstack((lons.flatten(),lats.flatten())).T
        tshape = np.shape(lons)
        inside = []
        
        for i in range(len(points)):
            inside.append(p.contains_point(points[i]))
            
        inside = np.array(inside, dtype=bool).reshape(tshape)
        index = np.where(inside==True)
        
        '''check if there are no points inside the given area'''        
        
        if not index[0].tolist():          # bbox covers no area
            raise Exception('no points in this area')
            
        else:
            return index
            
    def nearest_point_index(self, lon, lat, lons, lats, length=1,num=4):
        '''
        Return the index of the nearest rho point.
        lon, lat: the coordinate of start point, float
        lats, lons: the coordinate of points to be calculated.
        length: the boundary box.
        '''
        bbox = [lon-length, lon+length, lat-length, lat+length]
        index = self.bbox2ij(lons, lats, bbox)
        lon_covered = lons[index]
        lat_covered = lats[index]
        cp = np.cos(lat_covered*np.pi/180.)
        dx = (lon-lon_covered)*cp
        dy = lat-lat_covered
        dist = dx*dx+dy*dy

        # get several nearest points
        dist_sort = np.sort(dist)[0:9]
        findex = np.where(dist==dist_sort[0])
        lists = [[]] * len(findex)
        
        for i in range(len(findex)):
            lists[i] = findex[i]
            
        if num > 1:
            for j in range(1,num):
                t = np.where(dist==dist_sort[j])
                for i in range(len(findex)):
                     lists[i] = np.append(lists[i], t[i])
        indx = [i[lists] for i in index]
        return indx, dist_sort[0:num]
        '''
        for only one point returned
        mindist = np.argmin(dist)
        indx = [i[mindist] for i in index]
        return indx, dist[mindist]
        '''
        
    def get_track(self, timeperiod, data):
        pass
    
class get_roms(track):
    '''
    ####(2009.10.11, 2013.05.19):version1(old) 2009-2013
    ####(2013.05.19, present): version2(new) 2013-present
    (2006.01.01 01:00, 2014.1.1 00:00)
    '''
    
    def __init__(self):
        pass
        
    def get_url(self, starttime, endtime):
        '''
        get url according to starttime and endtime.
        '''
        self.starttime = starttime
        
        url_oceantime = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2006_da/his?ocean_time[0:1:69911]'
        data_oceantime = netCDF4.Dataset(url_oceantime)
        t1 = (starttime - datetime(2006,01,01,0,0,0,0,pytz.utc)).total_seconds()
        t2 = (endtime - datetime(2006,01,01,0,0,0,0,pytz.utc)).total_seconds()
        index1 = self.__closest_num(t1,data_oceantime.variables['ocean_time'][:])
        index2 = self.__closest_num(t2,data_oceantime.variables['ocean_time'][:])
        url = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2006_da/his?h[0:1:81][0:1:129],s_rho[0:1:35],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],mask_rho[0:1:81][0:1:129],u[{0}:1:{1}][0:1:35][0:1:81][0:1:128],v[{0}:1:{1}][0:1:35][0:1:80][0:1:129]'
        url = url.format(index1, index2)
        return url
        
    def __closest_num(self, num, numlist, i=0):
        '''
        Return index of the closest number in the list
        '''
        index1, index2 = 0, len(numlist)
        indx = int(index2/2)
        if not numlist[0] < num < numlist[-1]:
            raise Exception('{0} is not in {1}'.format(str(num), str(numlist)))
            
        if index2 == 2:
            l1, l2 = num-numlist[0], numlist[-1]-num
            
            if l1 < l2:
                i = i
                
            else:
                i = i+1
                
        elif num == numlist[indx]:
            i = i + indx
            
        elif num > numlist[indx]:
            i = self.__closest_num(num, numlist[indx:],
                              i=i+indx)
                              
        elif num < numlist[indx]:
            i = self.__closest_num(num, numlist[0:indx+1], i=i)
        return i
        
    def get_data(self, url):
        '''
        return the data needed.
        url is from get_roms.get_url(starttime, endtime)
        '''
        data = jata.get_nc_data(url, 'lon_rho', 'lat_rho', 'mask_rho','u', 'v', 'h', 's_rho')
        return data
        
    def get_track(self, lon, lat, depth, url):
        '''
        get the nodes of specific time period
        lon, lat: start point
        url: get from get_url(starttime, endtime)
        depth: 0~35, the 36th is the bottom.
        '''
        self.startpoint = lon, lat
        if type(url) is str:
            nodes = self.__get_track(lon, lat, depth, url)
            
        else:                                                                # case where there are two urls, one for start and one for stop time
            nodes = dict(lon=[self.startpoint[0]],lat=[self.startpoint[1]])
            
            for i in url:
                temp = self.__get_track(nodes['lon'][-1], nodes['lat'][-1], depth, i)
                nodes['lon'].extend(temp['lon'][1:])
                nodes['lat'].extend(temp['lat'][1:])
                
        return nodes # dictionary of lat and lon
        
    def __get_track(self, lon, lat, depth, url):
        '''
        return points
        '''
        data = self.get_data(url)
        nodes = dict(lon=lon, lat=lat)
        mask = data['mask_rho'][:]
        lon_rho = data['lon_rho'][:]
        lat_rho = data['lat_rho'][:]
        lons, lats = lon_rho[:-2, :-2], lat_rho[:-2, :-2]
        index, nearestdistance = self.nearest_point_index(lon,lat,lons,lats)
        depth_layers = data['h'][index[0][0]][index[1][0]]*data['s_rho']
        layer = np.argmin(abs(depth_layers+depth))
        u = data['u'][:,layer]
        v = data['v'][:,layer]
        
        for i in range(0, len(u)):
            u_t = u[i][:-2, :]
            v_t = v[i][:,:-2]
            u_p = u_t[index[0][0]][index[1][0]]
            v_p = v_t[index[0][0]][index[1][0]]

            if not u_p or not v_p:
                print 'point hit the land'
                break
            
            dx = 60*60*float(u_p)
            dy = 60*60*float(v_p)
            lon = lon + dx/(111111*np.cos(lat*np.pi/180))
            lat = lat + dy/111111
            index, nearestdistance = self.nearest_point_index(lon,lat,lons,lats)
            nodes['lon'] = np.append(nodes['lon'],lon)
            nodes['lat'] = np.append(nodes['lat'],lat)
        return nodes
        
class get_fvcom(track):
    def __init__(self, mod):
        self.modelname = mod
        
    def get_url(self, starttime, endtime):
        '''
        get different url according to starttime and endtime.
        urls are monthly.
        '''
        self.hours = int((endtime-starttime).total_seconds()/60/60)
        
        if self.modelname is "30yr":
            url = []
            time1 = datetime(2011,1,1,0,0,0,0,pytz.utc)                      #all these datetime are made based on the model.
            time2 = datetime(2011,11,11,0,0,0,0,pytz.utc)                    #The model use different version data of different period.
            time3 = datetime(2013,5,9,0,0,0,0,pytz.utc)
            time4 = datetime(2013,12,1,0,0,0,0,pytz.utc)                     
                        
            if endtime < time1:
                yearnum = starttime.year-1981
                standardtime = datetime.strptime(str(starttime.year)+'-01-01 00:00:00',
                                                 '%Y-%m-%d %H:%M:%S')
                print yearnum
                index1 = int(26340+35112*(yearnum/4)+8772*(yearnum%4)+1+self.hours)
                index2 = index1 + self.hours
                furl = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?h[0:1:48450],lat[0:1:48450],latc[0:1:90414],lon[0:1:48450],lonc[0:1:90414],u[{0}:1:{1}][0:1:44][0:1:90414],v[{0}:1:{1}][0:1:44][0:1:90414],siglay'
                url.append(furl.format(index1, index2)) 
                
            elif time1 <= endtime < time2: # endtime is in GOM3_v11
                url.extend(self.__temp(starttime,endtime,time1,time2))
            elif time2 <= endtime < time3:  # endtime is in GOM3_v12
                url.extend(self.__temp(starttime,endtime,time2,time3))
                
            elif time3 <= endtime < time4:
                url.extend(self.__temp(starttime,endtime,time3,time4))
                
        elif self.modelname is "GOM3":
            # I corrected this address on 10 July 2014 (JiM)
            url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc?lon[0:1:51215],lat[0:1:51215],lonc[0:1:95721],latc[0:1:95721],siglay[0:1:39][0:1:51215],h[0:1:51215],u[{0}:1:{1}][0:1:39][0:1:95721],v[{0}:1:{1}][0:1:39][0:1:95721]'
            current_time = pytz.utc.localize(datetime.now().replace(hour=0,minute=0))
            period = starttime-\
                     (current_time-timedelta(days=2))
                     #(current_time-timedelta(days=3))
            index1 = int(period.total_seconds()/60/60)
            index2 = index1 + self.hours
            url = url.format(index1, index2)
            
        elif self.modelname is "massbay":
            url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Forecasts/NECOFS_FVCOM_OCEAN_MASSBAY_FORECAST.nc?lon[0:1:98431],lat[0:1:98431],lonc[0:1:165094],latc[0:1:165094],siglay[0:1:9][0:1:98431],h[0:1:98431],u[{0}:1:{1}][0:1:9][0:1:165094],v[{0}:1:{1}][0:1:9][0:1:165094]'
            current_time = pytz.utc.localize(datetime.now().replace(hour=0,minute=0))
            period = starttime-\
                     (current_time-timedelta(days=3))
            index1 = int(period.total_seconds()/60/60)
            index2 = index1 + self.hours
            url = url.format(index1, index2)
        print url   
        return url
        
    def __temp(self, starttime, endtime, time1, time2):
        '''
        ????? Retrieves times from website?
        '''
        if time1 <= endtime < time2:
            pass
        else:
            
            sys.exit('{0} not in the right period'.format(endtime))
        url = []
        
        if starttime >= time1:    #start time is from 2011.11.10 as v12
        
            if starttime.month == endtime.month:
                
                url.append(self.__url(starttime.year,starttime.month,
                                            [starttime.day,starttime.hour],
                                            [endtime.day,endtime.hour]))
                                            
            else:
                
                if starttime.year == endtime.year:
                    y = starttime.year
                    
                    for i in range(starttime.month, endtime.month+1):
                        
                        if i == starttime.month:
                            url.append(self.__url(y,i,
                                                  [starttime.day, starttime.hour],
                                                  [calendar.monthrange(y,i)[1],0]))
                                                  
                        elif starttime.month < i < endtime.month:
                            url.append(self.__url(y,i,[1,0],
                                                  [calendar.monthrange(y,i)[1],0]))
                                                  
                        elif i == endtime.month:
                            url.append(self.__url(y,i,[1,0],
                                                  [endtime.day,endtime.hour]))
                                                  
                else:
                    
                    for i in range(starttime.year, endtime.year+1):
                        
                        if i == starttime.year:
                            url.extend(self.get_url(starttime,
                                               datetime(year=i,
                                                        month=12,day=31)))
                        elif i == endtime.year:
                            
                            url.extend(self.get_url(datetime(year=i,month=1,day=1),
                                               endtime))
                                               
                        else:
                            url.extend(self.get_url(datetime(year=i,month=1,day=1),
                                               datetime(year=i,month=12,day=31)))
             
        else:
            url.extend(self.get_url(starttime,(time1-timedelta(minutes=1))))
            url.extend(self.get_url(time1,endtime))
            
        return url
        
    def __url(self, year, month, start_daytime, end_daytime):
        '''
        start_daytime,end_daytime: [day,hour]
        '''
        
        url_v11 = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM3_{0}/gom3v11_{0}{1}.nc?lon[0:1:48727],lat[0:1:48727],lonc[0:1:90997],latc[0:1:90997],h[0:1:48727],u[{2}:1:{3}][0:1:39][0:1:90997],v[{2}:1:{3}][0:1:39][0:1:90997],siglay[0:1:39][0:1:48727]'
        url_v12 = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM3_{0}/gom3v12_{0}{1}.nc?lon[0:1:48859],lat[0:1:48859],lonc[0:1:91257],latc[0:1:91257],h[0:1:48859],u[{2}:1:{3}][0:1:39][0:1:91257],v[{2}:1:{3}][0:1:39][0:1:91257],siglay[0:1:39][0:1:48859]'
        url_v13 = 'http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_GOM3_{0}/gom3v13_{0}{1}.nc?lon[0:1:51215],lat[0:1:51215],lonc[0:1:95721],latc[0:1:95721],h[0:1:51215],u[{2}:1:{3}][0:1:39][0:1:95721],v[{2}:1:{3}][0:1:39][0:1:95721],siglay[0:1:39][0:1:51215]'
        time1 = datetime(year=2011,month=1,day=1)      #all these datetime are made based on the model.
        time2 = datetime(year=2011,month=11,day=11)      #The model use different version data of different period.
        time3 = datetime(year=2013,month=05,day=9)
        time4 = datetime(year=2013,month=12,day=1)
        currenttime = datetime(year=year,month=month,day=start_daytime[0])
                                       
        if time1 <= currenttime < time2:
            version = '11'
            
        elif time2 <= currenttime < time3:
            version = '12'
            
        elif time3 <= currenttime < time4:
            version = '13'

        if year == 2011 and month == 11  and start_daytime[0] >10:
            start = str(24*(start_daytime[0]-1)+start_daytime[1]-240)
            end = str(24*(end_daytime[0]-1)+end_daytime[1]-240)
            
        elif year == 2013 and month == 5 and start_daytime[0] >8:
            start = str(24*(start_daytime[0]-1)+start_daytime[1]-192)
            end = str(24*(end_daytime[0]-1)+end_daytime[1]-192)
            
        else:
            start = str(24*(start_daytime[0]-1)+start_daytime[1])
            end = str(24*(end_daytime[0]-1)+end_daytime[1])

        year = str(year)
        month = '{0:02d}'.format(month)
        
        if version == '11':
            url = url_v11.format(year, month, start, end)
            
        elif version == '12':
            url = url_v12.format(year, month, start, end)
            
        elif version == '13':
            url = url_v13.format(year, month, start, end)
            
        return url
        
    def get_data(self,url):
        '''
        ??? Retrieves data?
        '''
        self.data = jata.get_nc_data(url,'lon','lat','latc','lonc',
                                     'u','v','siglay','h')
        return self.data
        
    def get_track(self, lon, lat, depth, url):
        '''
        ???????
        '''
        if type(url) is str:
            nodes = dict(lon=[lon],lat=[lat])
            temp = self.__get_track(lon, lat, depth, url)
            nodes['lon'].extend(temp['lon'])
            nodes['lat'].extend(temp['lat'])
            
        else:
            nodes = dict(lon=[lon],lat=[lat])
            
            for i in url:
                temp = self.__get_track(nodes['lon'][-1], nodes['lat'][-1], depth, i)
                nodes['lat'].extend(temp['lat'])
                nodes['lon'].extend(temp['lon'])
                
        return nodes
        
    def __get_track(self, lon, lat, depth, url):
        '''
        start, end: indices of some period
        data: a dict that has 'u' and 'v'
        '''
        data = self.get_data(url)
        lonc, latc = data['lonc'][:], data['latc'][:]
        lonv, latv = data['lon'][:], data['lat'][:]
        h = data['h'][:]
        siglay = data['siglay'][:]
        
        if lon>90:
            lon, lat = dm2dd(lon, lat)
        nodes = dict(lon=[], lat=[])
        kf,distanceF = self.nearest_point_index(lon,lat,lonc,latc,num=1)
        kv,distanceV = self.nearest_point_index(lon,lat,lonv,latv,num=1)
        
        if h[kv] < 0:
            sys.exit('Sorry, your position is on land, please try another point')
        depth_total = siglay[:,kv]*h[kv]
        
###########################layer#####################################
        '''
        ????? Layer for what?????
        '''
        layer = np.argmin(abs(depth_total-depth))
            
        for i in range(self.hours):
            u_t = data['u'][i, layer, kf[0][0]]
            v_t = data['v'][i, layer, kf[0][0]]
            #print 'u_t, v_t, i', u_t, v_t, i
            dx = 60*60*u_t
            dy = 60*60*v_t
            lon = lon + (dx/(111111*np.cos(lat*np.pi/180)))
            lat = lat + dy/111111
            nodes['lon'].append(lon)
            nodes['lat'].append(lat)
            kf, distanceF = self.nearest_point_index(lon, lat, lonc, latc,num=1)
            kv, distanceV = self.nearest_point_index(lon, lat, lonv, latv,num=1)
            # depth_total = siglay[:][kv]*h[kv]
            
            if distanceV>=.3:
                
                if i==start:
                    print 'Sorry, your start position is NOT in the model domain'
                    break
                
        return nodes
        
class get_drifter(track):

    def __init__(self, drifter_id,filename=None):
        self.drifter_id = drifter_id
        self.filename = filename
    def get_track(self, starttime=None, days=None):
        '''
        return drifter nodes
        if starttime is given, return nodes started from starttime
        if both starttime and days are given, return nodes of the specific time period
        '''
        if filename:
            temp=getrawdrift(self.drifter_id,self.filename)
        else:
            temp = getdrift(self.drifter_id)
        nodes = {}
        
        nodes['lon'] = np.array(temp[1])
        nodes['lat'] = np.array(temp[0])
        nodes['time'] = np.array(temp[2])
        #starttime = np.array(temp[2][0])
        starttime = np.array(temp[2][-1]- timedelta(days=2)) # make start day 3 days before last fix
        print starttime
        if bool(starttime):
            
            if bool(days):
                endtime = starttime + timedelta(days=days)
                i = self.__cmptime(starttime, nodes['time'])
                j = self.__cmptime(endtime, nodes['time'])
                nodes['lon'] = nodes['lon'][i:j+1]
                nodes['lat'] = nodes['lat'][i:j+1]
                nodes['time'] = nodes['time'][i:j+1]
                
            else:
                i = self.__cmptime(starttime, nodes['time'])
                nodes['lon'] = nodes['lon'][i:-1]
                nodes['lat'] = nodes['lat'][i:-1]
                nodes['time'] = nodes['time'][i:-1]
                
        return nodes
        
    def __cmptime(self, time, times):
        '''
        return indies of specific or nearest time in times.
        '''
        tdelta = []
        
        for t in times:
            tdelta.append(abs((time-t).total_seconds()))
            
        index = tdelta.index(min(tdelta))
        
        return index
        
class get_roms_rk4(get_roms):
    '''
    model roms using Runge Kutta
    '''
    def get_track(self, lon, lat, depth, url):
        '''
        get the nodes of specific time period
        lon, lat: start point
        url: get from get_url(starttime, endtime)
        depth: 0~35, the 36th is the bottom.
        '''
        self.startpoint = lon, lat
        
        if type(url) is str:
            nodes = self.__get_track(lon, lat, depth, url)
            
        else: # case where there are two urls, one for start and one for stop time
            nodes = dict(lon=[self.startpoint[0]],lat=[self.startpoint[1]])
            
            for i in url:
                temp = self.__get_track(nodes['lon'][-1], nodes['lat'][-1], depth, i)
                nodes['lon'].extend(temp['lon'][1:])
                nodes['lat'].extend(temp['lat'][1:])
                
        return nodes # dictionary of lat and lon
        
    def __get_track(self, lon, lat, depth, url):
        '''
        ???? ????
        '''
        data = self.get_data(url)
        nodes = dict(lon=lon, lat=lat)
        mask = data['mask_rho'][:]
        lon_rho = data['lon_rho'][:]
        lat_rho = data['lat_rho'][:]
        index, nearestdistance = self.nearest_point_index(lon,lat,lons,lats)
        depth_layers = data['h'][index[0][0]][index[0][1]]*data['s_rho']
        layer = np.argmin(abs(depth_layers+depth))
        u = data['u'][:,layer]
        v = data['v'][:,layer]
        
        for i in range(0, len(data['u'][:])):
            u_t = u[i, :-2, :]
            v_t = v[i, :, :-2]
            lon, lat, u_p, v_p = self.RungeKutta4_lonlat(lon,lat,lons,lats,u_t,v_t)
            
            if not u_p:
                print 'point hit the land'
                break
            nodes['lon'] = np.append(nodes['lon'],lon)
            nodes['lat'] = np.append(nodes['lat'],lat)
            
        return nodes
        
    def polygonal_barycentric_coordinates(self,xp,yp,xv,yv):
        '''
        ??? how is this one solved???
        '''
        N=len(xv)   
        j=np.arange(N)
        ja=(j+1)%N
        jb=(j-1)%N
        Ajab=np.cross(np.array([xv[ja]-xv[j],yv[ja]-yv[j]]).T,
                      np.array([xv[jb]-xv[j],yv[jb]-yv[j]]).T)
        Aj=np.cross(np.array([xv[j]-xp,yv[j]-yp]).T,
                    np.array([xv[ja]-xp,yv[ja]-yp]).T)
        Aj=abs(Aj)
        Ajab=abs(Ajab)
        Aj=Aj/max(abs(Aj))
        Ajab=Ajab/max(abs(Ajab))    
        w=xv*0.
        j2=np.arange(N-2)
        
        for j in range(N):
            
            w[j]=Ajab[j]*Aj[(j2+j+1)%N].prod()
          
        w=w/w.sum()
        
        return w
        
    def VelInterp_lonlat(self,lonp,latp,lons,lats,u,v):
        '''
    # find the nearest vertex    
        kv,distance=nearlonlat(Grid['lon'],Grid['lat'],lonp,latp)
     #   print kv,lonp,latp
    # list of triangles surrounding the vertex kv    
        kfv=Grid['kfv'][0:Grid['nfv'][kv],kv]
    # coordinates of the (dual mesh) polygon vertices: the centers of triangle faces
        lonv=Grid['lonc'][kfv];latv=Grid['latc'][kfv]
        w=polygonal_barycentric_coordinates(lonp,latp,lonv,latv)
    # baricentric coordinates are invariant wrt coordinate transformation (xy - lonlat), check!    
    # interpolation within polygon, w - normalized weights: w.sum()=1.    
    # use precalculated Lame coefficients for the spherical coordinates
    # coslatc[kfv] at the polygon vertices
    # essentially interpolate u/cos(latitude)
    # this is needed for RungeKutta_lonlat: dlon = u/cos(lat)*tau, dlat = vi*tau
        cv=Grid['coslatc'][kfv]
     #   print cv    
        urci=(u[kfv]/cv*w).sum()
        vi=(v[kfv]*w).sum()
        return urci,vi
        '''
        index, distance = self.nearest_point_index(lonp,latp,lons,lats)
        lonv,latv = lons[index[0],index[1]], lats[index[0],index[1]]
        w = self.polygonal_barycentric_coordinates(lonp,latp,lonv,latv)
        uf = (u[index[0],index[1]]/np.cos(lats[index[0],index[1]]*np.pi/180)*w).sum()
        vf = (v[index[0],index[1]]*w).sum()
        
        return uf, vf
        
    def RungeKutta4_lonlat(self,lon,lat,lons,lats,u,v):
        '''
        ?????????????
        '''
        tau = 60*60/111111.
        lon1=lon*1.;          lat1=lat*1.;        urc1,v1=self.VelInterp_lonlat(lon1,lat1,lons,lats,u,v);  
        lon2=lon+0.5*tau*urc1;lat2=lat+0.5*tau*v1;urc2,v2=self.VelInterp_lonlat(lon2,lat2,lons,lats,u,v);
        lon3=lon+0.5*tau*urc2;lat3=lat+0.5*tau*v2;urc3,v3=self.VelInterp_lonlat(lon3,lat3,lons,lats,u,v);
        lon4=lon+    tau*urc3;lat4=lat+    tau*v3;urc4,v4=self.VelInterp_lonlat(lon4,lat4,lons,lats,u,v);
        lon=lon+tau/6.*(urc1+2.*urc2+2.*urc3+urc4);
        lat=lat+tau/6.*(v1+2.*v2+2.*v3+v4); 
        uinterplation=  (urc1+2.*urc2+2.*urc3+urc4)/6    
        vinterplation= (v1+2.*v2+2.*v3+v4)/6
       
        return lon,lat,uinterplation,vinterplation

def min_data(*args):
    '''
    return the minimum of several lists
    '''
    data = []

    for i in range(len(args)):
    
        data.append(min(args[i]))
        
    return min(data)
    
def max_data(*args):
    '''
    return the maximum of several lists
    '''
    data = []
    
    for i in range(len(args)):

        data.append(max(args[i]))
        
    return max(data)
    
def angle_conversion(a):
    '''
    converts the angle into radians
    '''
    a = np.array(a)
    
    return a/180*np.pi
    
def dist(lon1, lat1, lon2, lat2):
    '''
    calculate the distance of points
    '''
    R = 6371.004
    lon1, lat1 = angle_conversion(lon1), angle_conversion(lat1)
    lon2, lat2 = angle_conversion(lon2), angle_conversion(lat2)
    l = R*np.arccos(np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2)+
                    np.sin(lat1)*np.sin(lat2))
                    
    return l
    
def draw_basemap(fig, ax, lonsize, latsize, interval_lon=0.5, interval_lat=0.5):
    '''
    draw the basemap?
    '''
    ax = fig.sca(ax)
    dmap = Basemap(projection='cyl',
                   llcrnrlat=min(latsize)-0.01,
                   urcrnrlat=max(latsize)+0.01,
                   llcrnrlon=min(lonsize)-0.01,
                   urcrnrlon=max(lonsize)+0.01,
                   resolution='i',ax=ax)
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0])
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1])
    dmap.drawcoastlines()
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()

##############################################################
'''''''''''''''''''''''''MAIN PROGRAM'''''''''''''''''''''''''
##############################################################

''' initialize constants'''
#'115410701','118410701'
#drifter_ids = ['108410712','108420701','110410711','110410712','110410713','110410714',
#               '110410715','110410716','114410701','115410701','115410702']                                                  # Default drifter ID
#drifter_ids = ['115410701','118410701']#,'119410714','135410701','110410713','119410716']
drifter_ids = ['146410702']
mod = 'GOM3'                                                             # mod has to be '30yr' or 'GOM3' or 'massbay'
filename='drift_whoi_2014_1.dat'
depth = -1
days = 4.
starttime = datetime(2011,5,12,13,0,0,0,pytz.UTC)

for ID in drifter_ids:
    if filename:
         drifter = get_drifter(ID,filename)                                                # Retrive drifter data
    else:
         drifter = get_drifter(ID)
    print ID
    if starttime:

         if days:
             nodes_drifter = drifter.get_track(starttime,days)

         else:
            nodes_drifter = drifter.get_track(starttime)
        
    else:
        nodes_drifter = drifter.get_track()
    #print nodes_drifter   
    ''' determine latitude, longitude, start, and end times of the drifter?'''     

    lon, lat = nodes_drifter['lon'][0], nodes_drifter['lat'][0]
    # adjust for the added 5 hours in the models
    starttime = nodes_drifter['time'][0]#-timedelta(hours=5)
    endtime = nodes_drifter['time'][-1]#-timedelta(hours=5)
    #print starttime

    ''' read data points from fvcom and roms websites and store them'''
    get_fvcom_obj = get_fvcom(mod)
    url_fvcom = get_fvcom_obj.get_url(starttime, endtime)
    nodes_fvcom = get_fvcom_obj.get_track(lon,lat,depth,url_fvcom)           # iterates fvcom's data
    #get_roms_obj = get_roms()
    #url_roms = get_roms_obj.get_url(starttime, endtime)
    #nodes_roms = get_roms_obj.get_track(lon, lat, depth, url_roms)
    
    #if type(nodes_roms['lat']) == np.float64:                             # ensures that the single point case still functions properly
    
      #  nodes_roms['lon'] = [nodes_roms['lon']] 
       # nodes_roms['lat'] = [nodes_roms['lat']]
    
    '''Calculate the distance seperation'''

    #dist_roms = distance((nodes_drifter['lat'][-1],nodes_drifter['lon'][-1]),(nodes_roms['lat'][-1],nodes_roms['lon'][-1]))
    dist_fvcom = distance((nodes_drifter['lat'][-1],nodes_drifter['lon'][-1]),(nodes_fvcom['lat'][-1],nodes_fvcom['lon'][-1]))
    #print 'The seperation of roms was %f and of fvcom was %f kilometers for drifter %s' % (dist_roms[0], dist_fvcom[0], ID )

    ''' set latitude and longitude arrays for basemap'''

    lonsize = [min_data(nodes_drifter['lon'],nodes_fvcom['lon']),
             max_data(nodes_drifter['lon'],nodes_fvcom['lon'])]
    latsize = [min_data(nodes_drifter['lat'],nodes_fvcom['lat']),
             max_data(nodes_drifter['lat'],nodes_fvcom['lat'])]
             
    diff_lon = (lonsize[0]-lonsize[1])*4   
    diff_lat = (latsize[1]-latsize[0])*4      
    
    lonsize = [lonsize[0]-diff_lon,lonsize[1]+diff_lon]
    latsize = [latsize[0]-diff_lat,latsize[1]+diff_lat]
           
    ''' Plot the drifter track, model outputs form fvcom and roms, and the basemap'''           
      
    fig = plt.figure()
    ax = fig.add_subplot(111)
    draw_basemap(fig, ax, lonsize, latsize)
    ax.plot(nodes_drifter['lon'],nodes_drifter['lat'],'ro-',label='drifter')
    ax.plot(nodes_fvcom['lon'],nodes_fvcom['lat'],'yo-',label='fvcom')
    #ax.plot(nodes_roms['lon'],nodes_roms['lat'], 'go-', label='roms')
    ax.plot(nodes_drifter['lon'][0],nodes_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
    plt.title('ID: {0}   {1}   {2} days'.format(ID, starttime.strftime("%Y-%m-%d"), days))
    plt.legend(loc='lower right')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
    plt.savefig('plots/'+str(ID)+'.png')
    
