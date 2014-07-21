# -*- coding: utf-8 -*-
"""
Routine to compare Study Fleet TDR data with models
Created on Apr 8, 2013
@author: J Manning
"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import float64
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd
import sys
import netCDF4
from matplotlib import path
from dateutil import rrule
# import our local modules
sys.path.append('../modules')
import jmath,jata
from conversions import dm2dd,f2c
from utilities import my_x_axis_format

# First, a set of ROMS-related functions ####################################
class water(object):
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
        # inside = p.contains_points(points).reshape((n,m))
        inside = []
        for i in range(len(points)):
            inside.append(p.contains_point(points[i]))
        inside = np.array(inside, dtype=bool).reshape(tshape)
        # ii,jj = np.meshgrid(xrange(m),xrange(n))
        index = np.where(inside==True)
        if not index[0].tolist():          # bbox covers no area
            #raise Exception(''')
             print 'no points in this area'
             index=0
        else:
            # points_covered = [point[index[i]] for i in range(len(index))]
            # for i in range(len(index)):
                # p.append(point[index[i])
            # i0,i1,j0,j1 = min(index[1]),max(index[1]),min(index[0]),max(index[0])
         return index
    def nearest_point_index(self, lon, lat, lons, lats, length=(1, 1)):
        '''
        Return the index of the nearest rho point.
        lon, lat: the coordinate of start point, float
        lats, lons: the coordinate of points to be calculated.
        length: the boundary box.
        '''
        bbox = [lon-length[0], lon+length[0], lat-length[1], lat+length[1]]
        index = self.bbox2ij(lons, lats, bbox)
        lon_covered = lons[index]
        lat_covered = lats[index]
        cp = np.cos(lat_covered*np.pi/180.)
        dx = (lon-lon_covered)*cp
        dy = lat-lat_covered
        dist = dx*dx+dy*dy
        mindist = np.argmin(dist)
        indx = [i[mindist] for i in index]
        return indx, dist[mindist]
class water_roms(water):
   '''
    ####(2009.10.11, 2013.05.19):version1(old) 2009-2013
    ####(2013.05.19, present): version2(new) 2013-present
    (2006.01.01 01:00, present)
    ''' 
   def get_url(self, starttime, endtime):
        '''
        get url according to starttime and endtime.
        '''
        self.starttime = starttime
        #self.hours = int((endtime-starttime).total_seconds()/60/60) # get total hours
        #time_r = dt(year=2006,month=1,day=9,hour=1,minute=0)
        url_oceantime = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2006_da/his?ocean_time'
        data_oceantime = netCDF4.Dataset(url_oceantime)
        #t1 = (starttime - dt(2006,01,01)).total_seconds()
        #t2 = (endtime - dt(2006,01,01)).total_seconds()
        t1 = (starttime - dt(2006,01,01)).total_seconds()
        t2 = (endtime - dt(2006,01,01)).total_seconds()
        index1 = self.__closest_num(t1,data_oceantime.variables['ocean_time'][:])
        index2 = self.__closest_num(t2,data_oceantime.variables['ocean_time'][:])
        url = 'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2006_da/his?h[0:1:81][0:1:129],s_rho[0:1:35],lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],mask_rho[0:1:81][0:1:129],temp[{0}:1:{1}][0:1:35][0:1:81][0:1:129],ocean_time[{0}:1:{1}]'
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
        url is from water_roms.get_url(starttime, endtime)
        '''
        #data = jata.get_nc_data(url, 'lon_rho', 'lat_rho', 'mask_rho','u', 'v', 'h', 's_rho')
        data = jata.get_nc_data(url, 'lon_rho', 'lat_rho', 'mask_rho','temp', 'h', 's_rho','ocean_time')
        return data
   def waternode(self, lon, lat, depth, url):
        '''
        return points
        '''
        data = self.get_data(url)
        nodes = dict(temp=[])
        mask = data['mask_rho'][:]
        lon_rho = data['lon_rho'][:]
        lat_rho = data['lat_rho'][:]
        lons = jata.shrink(lon_rho, mask[1:,1:].shape)
        lats = jata.shrink(lat_rho, mask[1:,1:].shape)
        print 'finding the nearest node ...'
        index, nearestdistance = self.nearest_point_index(lon,lat,lons,lats)
        depth_layers = data['h'][index[0]][index[1]]*data['s_rho']
        layer = np.argmin(abs(depth_layers-depth))
        print 'extracting modeled time'
        ot=data['ocean_time'][:]
        otdt=[] # datetime version of ocean_time
        for k in range(len(ot)):
           otdt.append(dt(2006,1,1,0,0)+td(seconds=ot[k]))
        print 'extracting modeled temperature for this depth and site'
        nodes=data['temp'][:,layer,index[0],index[1]]
        modtso=pd.DataFrame(nodes, index=otdt)
        return modtso


# Second, a set of FVCOM-related functions ###################################################
def nearlonlat(lon,lat,lonp,latp):
    """
    i,min_dist=nearlonlat(lon,lat,lonp,latp) change
    find the closest node in the array (lon,lat) to a point (lonp,latp)
    input:
        lon,lat - np.arrays of the grid nodes, spherical coordinates, degrees
        lonp,latp - point on a sphere
        output:
            i - index of the closest node
            min_dist - the distance to the closest node, degrees
            For coordinates on a plane use function nearxy
            
            Vitalii Sheremet, FATE Project
    """
    cp=np.cos(latp*np.pi/180.)
    # approximation for small distance
    dx=(lon-lonp)*cp
    dy=lat-latp
    dist2=dx*dx+dy*dy
    # dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    #min_dist=np.sqrt(dist2[i])
    return i#,min_dist 
   
def inconvexpolygon(xp,yp,xv,yv):
    """
check if point is inside a convex polygon

    i=inconvexpolygon(xp,yp,xv,yv)
    
    xp,yp - arrays of points to be tested
    xv,yv - vertices of the convex polygon

    i - boolean, True if xp,yp inside the polygon, False otherwise
    
    """    
    N=len(xv)   
    j=np.arange(N)
    ja=(j+1)%N # next vertex in the sequence 
#    jb=(j-1)%N # previous vertex in the sequence
    
    NP=len(xp)
    i=np.zeros(NP,dtype=bool)
    for k in range(NP):
        # area of triangle p,j,j+1
        print j
        print xv[j]
        print xp[k]
        Aj=np.cross(np.array([xv[j]-xp[k],yv[j]-yp[k]]).T,np.array([xv[ja]-xp[k],yv[ja]-yp[k]]).T) 
    # if a point is inside the convect polygon all these Areas should be positive 
    # (assuming the area of polygon is positive, counterclockwise contour)
        Aj /= Aj.sum()
    # Now there should be no negative Aj
    # unless the point is outside the triangular mesh
        i[k]=(Aj>0.).all()
        
    return i
def inmodel_roms(xp, yp):
    romsbottom_lat = 33.744605290701315
    romsbottom_lon = -75.838285993254701
    romstop_lat = 42.868821661800354
    romstop_lon = -71.429602344296995
    romsleft_lat = 36.952672662205458
    romsleft_lon = -79.588634504965825
    romsright_lat = 39.894586726296446
    romsright_lon = -67.707269419137802
    roms_xv = np.array([romstop_lon, romsright_lon, romsbottom_lon, romsleft_lon])
    roms_yv = np.array([romstop_lat, romsright_lat, romsbottom_lat, romsleft_lat])
    i = inconvexpolygon(xp, yp, roms_xv, roms_yv)
    return i
# Forth, the main program ############################################################################
fn='binned_td_test.csv'
direct='/net/data5/jmanning/hoey/' 
outputdir='/net/data5/jmanning/modvsobs/sfleet/'
# read in the study fleet data
def parse(datet):
   #print datet[0:10],datet[11:13],datet[14:16]
    dtt=dt.strptime(datet,'%Y-%m-%d:%H:%M')
    return dtt
obstso=pd.read_csv(direct+fn,sep=',',skiprows=0,parse_dates={'datet':[2]},index_col='datet',date_parser=parse,names=['LATITUDE','LONGITUDE','ROUND_DATE_TIME','OBSERVATIONS_TEMP','MEAN_TEMP','MIN_TEMP','MAX_TEMP','STD_DEV_TEMP','OBSERVATIONS_DEPTH','MEAN_DEPTH','MIN_DEPTH','MAX_DEPTH','STD_DEV_DEPTH','nan'])
#convert ddmm.m to dd.ddd
plt.figure(figsize=(16,10))
o=[]
m=[]
for k in range(len(obstso)): # 
        [la,lo]=dm2dd(obstso['LATITUDE'][k],obstso['LONGITUDE'][k])
        if not inmodel_roms([lo], [la]):
            print 'point not in roms domain'
            continue
        else:
           romobj = water_roms()
           modtso = pd.DataFrame()
           st=obstso.index[k]
           et=st+td(hours=1)
           url_roms = romobj.get_url(st,et )
           modtso= romobj.waternode(lo, la,-1*obstso['MEAN_DEPTH'][k], url_roms)
           o.append(obstso['MEAN_TEMP'][k])
           m.append(modtso.values[0])
           plt.plot(modtso.values[0],obstso['MEAN_TEMP'][k],'*', markersize=30)
plt.xlabel('MODEL (degC)')
plt.ylabel('OBSERVATIONS (degC)')
plt.title('Study Fleet vs ROMS ')
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/sfleetvsroms.png')

 
