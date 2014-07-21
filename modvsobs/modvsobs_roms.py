# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:15:34 2013
documented at http://www.nefsc.noaa.gov/epd/ocean/MainPage/py/modvsobs/html/index.html 
@author: Yacheng Wang and J Manning
"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import float64
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd
import pytz
import sys
import netCDF4
from matplotlib import path
from dateutil import rrule
# import our local modules
sys.path.append('../modules')
from getdata import getemolt_latlon,getobs_tempsalt
#sys.path.append('../../roms')
import jmath,jata
from conversions import dm2dd,f2c
from utilities import my_x_axis_format

######### HARDCODES ##############
#all sites are listed in /data5/jmanning/modvsobs/totalcalculate_41sites_list.dat and the following line
#site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
#site=['DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
#site=['MM01','OC01','OC02','OC03','JP01','JP02','JP03','JP13','JP14','JP19','JP22']
#site=['JP14','JP19','JP22']
#site=['MM01']
site=['OC01']
aorb='b_'
intime=[dt(2006,1,10,1,0,0,0,pytz.UTC),dt(2013,12,31,0,0,0,0,pytz.UTC)] # note ROMS starts on 1/10/2006
siteprocess=[]
depthinfor=[]
minnumperday=18
numperday=24
intend_to='temp'##############notice intend_to can be 'temp'or'salinity'
surf_or_bott='bott'
outputdir='/net/data5/jmanning/modvsobs/roms/'
color1='black'
############################################
if site=='MM01':
  aorb='a_'
else:
  aorb='b_'
if color1=='black':
  color2='gray'
else:
  color2='red'


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
            raise Exception('no points in this area')
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
        modtso = pd.DataFrame()
        # CHUNK THROUGH 6 months AT A TIME SINCE IT WAS HANGING UP OTHERWISE
        #for k in range(0,(endtime-starttime).days*24,365*24):
        for k in range(0,(endtime-starttime).days*24,182*24):
          #print 'Generating timeseries'
          #ts=var[modindex[0]:modindex[1],layer,inode]
          #print 'Generating time index'
          #idn=jd[modindex[0]:modindex[1]]
          #print 'Generating a dataframe of model data requested'
          #modtso=pd.DataFrame(ts,index=idn)
          print 'Generating a dataframe of model data requested from '+str(k)+' to ',str(k+182*24)
          #modtso=pd.DataFrame(var[modindex[0]:modindex[1],layer,inode],index=jd[modindex[0]:modindex[1]])
          modtso1=pd.DataFrame(var[modindex[0]+k:modindex[0]+k+182*24,layer,inode],index=jd[modindex[0]+k:modindex[0]+k+182*24])
          modtso=pd.concat([modtso,modtso1])
        return modtso
 
# Third, a set of Pandas averaging routines ###########################################################       
def resamda(oritso): 
        '''
        resample daily average data
        add some new columns like 'count mean,median,max,min,std,yy,mm,dd'
        '''     
        resamda=float64(oritso[0]).resample('D',how=['count','mean','median','min','max','std'])
        resamda.ix[resamda['count']<minnumperday,['mean','median','min','max','std']] = 'NaN'
        
        resamda['yy']=resamda.index.year
        resamda['mm']=resamda.index.month
        resamda['dd']=resamda.index.day
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resamdaf=resamda.reindex(columns=output_fmt)  
        return resamdaf

def resamma(oritso):
        '''
        resample month average data
        '''
        resamma=float64(oritso[0]).resample('m',how=['count','mean','median','min','max','std'],kind='period')
        resamma.ix[resamma['count']<25*numperday,['mean','median','min','max','std']] = 'NaN'
        resamma['yy']=resamma.index.year
        resamma['mm']=resamma.index.month
        resamma['dd']=15
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resammaf=resamma.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resammaf

def resamdc(resamda):
        '''
        resample daily climatology
        '''
        newindex=[]
        for j in range(len(resamda)):    
                newindex.append(resamda['mean'].index[j].replace(year=2000)) # puts all observations in the same year
        repd=pd.DataFrame(resamda['mean'].values,index=newindex)
        resamdc=repd[0].resample('D',how=['count','mean','median','min','max','std'])    #add columns for custom date format
        resamdc['yy']=0
        resamdc['mm']=resamdc.index.month
        resamdc['dd']=resamdc.index.day
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resamdcf=resamdc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resamdcf

def resammc(resamdc):
        '''
        resample month climatology
        '''
        resammc=resamdc['mean'].resample('m',how=['mean','median'],loffset=td(days=-15))
        resammc['count']=0
        resammc['min']=0.
        resammc['max']=0.
        resammc['std']=0.   
        recount=resamdc['count'].resample('m',how=['mean'],loffset=td(days=-15)).values
        remi=resamdc['min'].resample('m',how=['mean'],loffset=td(days=-15)).values
        rema=resamdc['max'].resample('m',how=['mean'],loffset=td(days=-15)).values
        restd=resamdc['std'].resample('m',how=['mean'],loffset=td(days=-15)).values
        for kk in range(len(resammc)):
           resammc['count'].values[kk]=recount[kk]
           resammc['min'].values[kk]=remi[kk]
           resammc['max'].values[kk]=rema[kk]
           resammc['std'].values[kk]=restd[kk]
        resammc['yy']=0
        resammc['mm']=resammc.index.month
        resammc['dd']=0
        output_fmt=['yy','mm','dd','count','mean','median','min','max','std']
        resammcf=resammc.reindex(columns=output_fmt)# found I needed to generate a new dataframe to print in this order
        return resammcf

def diffdadc(diff):
        day=[]
        for i in range(len(diff)):
            day.append(str(diff.index[i].year)+'-'+str(diffda.index[i].month)+'-'+str(diffda.index[i].day))
        #daydadctime=pd.DataFrame(day,index=diff.index)
        #diff=diff.join(daydadctime)
        #difff=diff.reindex(columns=output_fmt)
        diff['date']=day
        #diff.columns=['date','mean','median','min','max','std']
        diff=diff[['date','mean','median','min','max','std']]
        return diff

# Forth, the main program ############################################################################
for k in range(len(site)):
#################read-in obs data##################################
        print site[k]
        [lati,loni,bd]=getemolt_latlon(site[k]) # extracts lat/lon based on site code
        #[lati,loni]=dm2dd(lati,loni)#converts decimal-minutes to decimal degrees
        if surf_or_bott=='bott':
            #dept=[bd[0]-0.25*bd[0],bd[0]+.25*bd[0]]
            dept=[bd-0.25*bd,bd+.25*bd]
        else:
            dept=[0,5]
        #(obs_dt,obs_temp,obs_salt,distinct_dep)=getobs_tempsalt(site[k], input_time=[dt(2006,1,10,1,0),dt(2013,12,31,0,0)], dep=dept)
        (obs_dt,obs_temp,distinct_dep)=getobs_tempsalt(site[k], input_time=intime)
        #depthinfor.append(site[k]+','+str(bd[0])+','+str(distinct_dep)+'\n') # note that this distinct depth is actually the overall mean
        depthinfor.append(site[k]+','+str(bd)+','+str(distinct_dep)+'\n') # note that this distinct depth is actually the overall mean
        obs_dtindex=[]
        if intend_to=='temp':            
            for kk in range(len(obs_temp)):
                #obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius
                obs_dtindex.append(dt.strptime(str(obs_dt[kk])[:10],'%Y-%m-%d'))
            obstso=pd.DataFrame(obs_temp,index=obs_dtindex)
        else:
            for kk in range(len(obs_salt)):
                obs_dtindex.append(dt.strptime(str(obs_dt[kk])[:10],'%Y-%m-%d'))
            obstso=pd.DataFrame(obs_salt,index=obs_dtindex)   
        print 'observed Dataframe is ready'

##################generate resample DataFrame and putput file################################################
        reobsdaf=resamda(obstso)
        reobsmaf=resamma(obstso)
        reobsdcf=resamdc(reobsdaf)
        reobsmcf=resammc(reobsdcf)
        reobsdaf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_da_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        reobsmaf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_ma_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        reobsdcf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_dc_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        reobsmcf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_mc_obs.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
###################read-in mod data#################################

        starttime=obs_dt[0].replace(tzinfo=None)
        endtime=obs_dt[-1].replace(tzinfo=None)
        print starttime,endtime
        #try:
        romobj = water_roms()
        modtso = pd.DataFrame()
        # CHUNK THROUGH ~six months AT A TIME SINCE IT WAS HANGING UP OTHERWISE
        for j in range(0,(endtime-starttime).days*24,365*24):
                #print 'Generating a dataframe of model data requested from '+str(j)+' to ',str(j+365*24)
                et=starttime+td(hours=j+365*24)
                if et>endtime:
                   et=endtime
                print 'Generating a dataframe of model data requested from '+str(starttime+td(hours=j))+' to ',str(et)
                url_roms = romobj.get_url(starttime+td(hours=j),et )
                #nodes_roms= romobj.waternode(loni, lati, -1*bd, url_roms)
                modtso1= romobj.waternode(loni, lati, -1*bd, url_roms)
                print 'Creating a model dataframe...'
                #num_hours=len(nodes_roms)
                #times=list(rrule.rrule(rrule.HOURLY,count=num_hours,dtstart=starttime+td(hours=j)))
                #modtso1=pd.DataFrame(nodes_roms, index=times)
                modtso=pd.concat([modtso,modtso1])
        print 'now filter data to make daily obs and mod coincide.'
 
              
##############generate resample DataFrame and output file#############
        remoddaf=resamda(modtso) # daily averages
        remoddaf['mean'] += reobsdaf['mean']*0
        remoddaf['median'] += reobsdaf['median']*0
        remoddaf['min'] += reobsdaf['min']*0
        remoddaf['max'] += reobsdaf['max']*0
        remoddaf['std'] += reobsdaf['std']*0
        
        print 'now filter data to make monthly obs and mod coincide.'
        remodmaf=resamma(modtso) # monthly averages
        remodmaf['mean'] += reobsmaf['mean']*0
        remodmaf['median'] += reobsmaf['median']*0   
        remodmaf['min'] += reobsmaf['min']*0
        remodmaf['max'] += reobsmaf['max']*0
        remodmaf['std'] += reobsmaf['std']*0
        remoddcf=resamdc(remoddaf) #daily climatology
        remodmcf=resammc(remoddcf) # monthly climatology
        remoddaf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_da_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        remodmaf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_ma_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        remoddcf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_dc_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        remodmcf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_mc_mod.csv',index=False,header=False,na_rep='NaN',float_format='%10.2f')
        print 'now prepare plot'
          
            
##############plot da compare figure##################
        fig=plt.figure(figsize=(16,10))
        ax=fig.add_subplot(211)
        ax.plot_date(reobsdaf.index,reobsdaf['mean'],fmt='-',linewidth=2,color=color2)
        plt.grid()
        ax.plot_date(remoddaf.index,remoddaf['mean'],fmt='-',linewidth=2,color=color1)#bottom most value equals 44
        if intend_to=='temp':
             plt.ylabel('degree c')
        else:
             plt.ylabel('salinity')
             plt.title('eMOLT site '+site[k]+surf_or_bott+intend_to+' vs ROMS ')
             plt.legend(['observed','modeled'],loc='best')
###############plot mc compare figure##################
        TimeDelta=reobsmcf.index[-1]-reobsmcf.index[0]          
        ax1 = fig.add_subplot(212)
        my_x_axis_format(ax1, TimeDelta)
        ax1.plot_date(reobsmcf.index,reobsmcf['mean'],fmt='-',color=color2,linewidth=3)
        plt.grid()
        ax1.plot_date(remodmcf.index,remodmcf['mean'],fmt='-',color=color1,linewidth=3)#bottom most value equals 44
        if intend_to=='temp':
                plt.ylabel('degree c')
        else:
                plt.ylabel('salinity')
        plt.title('eMOLT site '+site[k]+surf_or_bott+intend_to+' vs ROMS ')
        plt.legend(['observed','modeled'],loc='best')
            
        plt.show()
        plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig14'+aorb+site[k]+surf_or_bott+intend_to+'_mod_obs.png')
        plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/fig14'+aorb+site[k]+surf_or_bott+intend_to+'_mod_obs.eps')
        plt.close()
            
############calculate the different#######################
        #output_fmt=[0,'mean','median','min','max','std']
        print 'Calculating differences in climatology'
        diffmc=reobsmcf-remodmcf
        diffmc['month']=range(1,13)
        #month=pd.DataFrame(range(1,13),index=diffmc.index)
        #diffmcf=diffmc.reindex(columns=output_fmt)
        #diffmc.columns=['month','mean','median','min','max','std']
        diffmc=diffmc[['month','mean','median','min','max','std']]
        diffmc.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_mc_mod_mc_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')

        print 'Calculating differences in mthly averages'
        diffma=reobsmaf-remodmaf
        date=[]
        for i in range(len(diffma)):
                date.append(str(diffma.index[i].year)+'-'+str(diffma.index[i].month))
        diffma['Year-Month']=date
        #datetimepd=pd.DataFrame(date,index=diffma.index)
        #diffma=diffma.join(datetimepd)
        #diffmaf=diffma.reindex(columns=output_fmt)
        #diffma.columns=['Year-Month','mean','median','min','max','std']
        diffma=diffma[['Year-Month','mean','median','min','max','std']]
        diffma.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_ma_mod_ma_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')

        print 'Calculating differences in daily averages & climatology'
        diffda=reobsdaf-remoddaf
        diffdc=reobsdcf-remoddcf

        diffdaf=diffdadc(diffda)
        diffdaf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_da_mod_da_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')
        diffdcf=diffdadc(diffdc)
        diffdcf.to_csv(outputdir+site[k]+surf_or_bott+intend_to+'_dc_mod_dc_obs.csv',index=False,header=True,na_rep='NaN',float_format='%10.2f')
        siteprocess.append(site[k])
        #except:
        #    print 'Can not get model data for this site.'
        #    #k+=1
        # del water_roms

print 'processed sites include'+str(siteprocess)+'.'
import pickle
f = open('/data5/jmanning/modvsobs/roms/ProcessedSite.csv', 'w')
pickle.dump(siteprocess, f)
f.close()
d=open('/data5/jmanning/modvsobs/roms/Depthinformation.csv','w')
pickle.dump(depthinfor,d)
d.close()
        
