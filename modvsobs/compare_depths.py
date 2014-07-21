# -*- coding: utf-8 -*-
"""
Created on Dec 17, 2013
@author: J Manning

Compares various measures of water depth (model, observed, fisherman-reported, etc)
"""



import numpy as np
import sys
import netCDF4
import matplotlib.pyplot as plt
# import our local modules
sys.path.append('../modules')
from getdata import getemolt_latlon
from conversions import dm2dd,distance,fth2m
from utilities import nearlonlat
from pydap.client import open_url
from models import get_dataset
from basemap import basemap_standard

def getemolt_latlon(site):
    """
    get data from emolt_site
    """
    urllatlon = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_site?emolt_site.SITE,emolt_site.LAT_DDMM,emolt_site.LON_DDMM,emolt_site.ORIGINAL_NAME,emolt_site.BTM_DEPTH&emolt_site.SITE='
    dataset = open_url(urllatlon+'"'+site+'"')
    print dataset
    var = dataset['emolt_site']
    lat = list(var.LAT_DDMM)
    lon = list(var.LON_DDMM)
    original_name = list(var.ORIGINAL_NAME)
    bd=fth2m(list(var.BTM_DEPTH)[0])
    #bd=fth2m(bd[0])
    return lat[0], lon[0], original_name,bd

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
    get the model depth for lat,lon
    """
    url = 'http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v1_0'
    index_lat, index_lon, basemap_topo = get_index_latlon(url,lat,lon)
    if index_lat == 0 or index_lon == 0:        
        url = 'http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc'
        index_lat, index_lon, basemap_topo = get_index_latlon(url,lat,lon)
    return basemap_topo.topo[index_lat, index_lon][0]

#def get_w_depth(xi, yi, url='http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc'):# xi is longitude,like [-69.2,-69.1].yi is latitude,like[41.0,41.1]
def get_w_depth(xi, yi, url='http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v1_0'):# xi is longitude,like [-69.2,-69.1].yi is latitude,like[41.0,41.1]
    try:
        dataset = open_url(url)
    
    except:
        print 'Sorry, ' + url + ' is not available'
        sys.exit(0)

    #read lat, lon,topo from url
    xgom_array = dataset['lon']
    ygom_array = dataset['lat']
    dgom_array = dataset['topo'].topo
    print np.shape(xgom_array),xgom_array[0],xi[0]
    #print dgom_array.shape, xgom_array[5:9],dgom_array[5]

    #convert the array to a list
    xgom, ygom = [], []
    
    for i in xgom_array:
        if i > xi[0] - 0.000834 and i < xi[0] + 0.000834:
        #if i > xi[0] - 0.0834 and i < xi[0] + 0.0834:
            xgom.append(i)
  
    for i in ygom_array:
        if i > yi[0] - 0.000834 and i < yi[0] + 0.000834:
        #if i > yi[0] - 0.0834 and i < yi[0] + 0.0834:
            ygom.append(i)
    print np.shape(xgom)        
    x_index, y_index = [], []
    (ys, xs) = dgom_array.shape

    for i in range(0, len(xgom)):
        x_index.append(int(round(np.interp(xgom[i], xgom_array, range(xs)))))
    for i in range(0, len(ygom)):
        y_index.append(int(round(np.interp(ygom[i], ygom_array, range(ys)))))
    
    dep, distkm, dist1 = [], [], []

    for k in range(len(x_index)):
        for j in range(len(y_index)):
            dep.append(dgom_array[(y_index[j], x_index[k])])
       
            #distkm, b = dist(ygom[j], xgom[k], yi[0], xi[0],)
            distkm, b = distance((ygom[j], xgom[k]),( yi[0], xi[0]))
            dist1.append(distkm)

    #get the nearest,second nearest,third nearest point.
    dist_f_nearest = sorted(dist1)[0]
    dist_s_nearest = sorted(dist1)[1]
    dist_t_nearest = sorted(dist1)[2]
    
    index_dist_nearest = range(len(dist1))
    index_dist_nearest.sort(lambda x, y:cmp(dist1[x], dist1[y]))
    
    dep_f_nearest = dep[index_dist_nearest[0]]
    dep_s_nearest = dep[index_dist_nearest[1]]
    dep_t_nearest = dep[index_dist_nearest[2]]

    #compute the finally depth
    d1 = dist_f_nearest
    d2 = dist_s_nearest
    d3 = dist_t_nearest
    def1 = dep_f_nearest
    def2 = dep_s_nearest
    def3 = dep_t_nearest
    depth_finally = def1 * d2 * d3 / (d1 * d2 + d2 * d3 + d1 * d3) + def2 * d1 * d3 / (d1 * d2 + d2 * d3 + d1 * d3) + def3 * d2 * d1 / (d1 * d2 + d2 * d3 + d1 * d3)

    return depth_finally[0]
site=['AB01','AG01','BA01','BA02','BC01','BD01','BF01','BI02','BI01','BM01','BM02','BN01','BS02','CJ01','CP01','DC01','DJ01','DK01','DMF1','ET01','GS01','JA01','JC01','JS06','JT04','KO01','MF02','MM01','MW01','NL01','PF01','PM02','PM03','PW01','RA01','RM02','RM04','SJ01','TA14','TA15','TS01']
#site=['MW01','DK01']
outf=open('/net/data5/jmanning/modvsobs/compare_depths.out','w')
fig=plt.figure()
cont_range=range(20,100,10)
#basemap_usgs([40.,45],[-72.,-65.],True,False,[0.5],list(np.array(cont_range)*-1))
#basemap_standard([40.,45.],[-72.,-65.],2)#True,False,[0.5],list(np.array(cont_range)*-1))
from mpl_toolkits.basemap import Basemap
lat=[40.,45.]
lon=[-71.,-65.]
comp='p_emoltvsmod'# this is the mode of comparison where p_ referes to percent difference
print comp
m = Basemap(projection='cyl',llcrnrlat=min(lat)-0.01,urcrnrlat=max(lat)+0.01,\
            llcrnrlon=min(lon)-0.01,urcrnrlon=max(lon)+0.01,resolution='h')
m.drawcoastlines()
m.fillcontinents(color='grey')
m.drawmapboundary()   
ebd,mbd,ubd,hbd=[],[],[],[]       
diffd=[]
outf.write('site,lon,lat,ebd,udb,hbd,mbd,perc_diff\n')
for k in range(len(site)):
  [elat, elon, original_name,eb]=getemolt_latlon(site[k])
  ebd.append(eb)
  [elat_dd,elon_dd]=dm2dd(elat,elon)
  mbd.append(getFVCOM_depth(elat_dd,elon_dd))
  ubd.append(-1*getdepth(elat_dd,elon_dd))#nearset usgs depth
  hbd.append(-1*get_w_depth( [elon_dd],[elat_dd]))#huanxins interpolated depth
  if comp=='usgsvsmod':
    diffd.append(ubd[k]-mbd[k])
  elif comp=='p_emoltvsmod':
    diffd.append((ebd[k]-mbd[k])/ebd[k]*100)  
  if diffd[k]<1:
      dotcol='magenta'
  else:
      dotcol='cyan'
  plt.scatter(elon_dd,elat_dd,25*abs(diffd[k]),marker='o',color=dotcol)
  
  #print 'ebd='+str(ebd)+'  ubd='+str(ubd)+' hbd='+str(hbd)+' mbd='+str(mbd)
  outf.write(site[k]+','+'%6.3f' % (elon_dd)+','+'%6.3f' % (elat_dd)+','+'%6.1f' % (ebd[k])+','+'%6.1f' % (mbd[k])+','+'%6.1f' % (ubd[k][0])+','+'%6.1f' % (hbd[k][0])+','+'%6.1f' % (diffd[k])+'\n')
outf.close()  
#plt.title('Obs-Model Bottom Depths Mean: '+'%6.1f' % (np.mean(diffd))+' and STD: '+'%6.1f' % (np.std(diffd)))
plt.title(comp+' Bottom Depths Mean: '+'%6.1f' % (np.mean(diffd))+' and STD: '+'%6.1f' % (np.std(diffd)))
plt.text(-69,41,'magenta>>negative',color='magenta')
plt.text(-69,40.75,'cyan>>positive',color='cyan')
if comp[0:3]=='emol':#tvsmod':
  plt.annotate('max difference = '+'%6.1f' % (max(abs(min(diffd)),max(diffd)))+' meters',xy=(-67.248,44.487),xytext=(-68,43.),arrowprops=dict(frac=0.3,facecolor='red', shrink=0.2))
elif comp[0:3]=='p_e':#moltvsmod':
  plt.annotate('max difference = '+'%6.1f' % (max(abs(min(diffd)),max(diffd)))+' %',xy=(-67.248,44.487),xytext=(-68,43.),arrowprops=dict(frac=0.3,facecolor='red', shrink=0.2))   
elif comp[0:3]=='usg':#svsmod':
  plt.annotate('max difference = '+'%6.1f' % (max(abs(min(diffd)),max(diffd)))+' meters',xy=(-69.067,40.062),xytext=(-68,40.5),arrowprops=dict(frac=0.3,facecolor='red', shrink=0.2))   
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/compare_depths_'+comp+'.png')

fig2=plt.figure()
bar_width=0.2
opacity = 0.4
plt.bar(np.arange(len(ebd)),ebd,bar_width,color='b',label='eMOLT')
plt.bar(np.arange(len(mbd))+bar_width,mbd,bar_width,color='r',label='GOM3')
plt.bar(np.arange(len(ubd))+2*bar_width,ubd,bar_width,color='g',label='USGS')
plt.legend()
plt.tight_layout()
plt.ylabel('Depth (m)')
plt.xlabel('Site')
plt.show()
plt.title('Comparing Estimates of Water Column Depth')
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/compare_depths_bar.png')
