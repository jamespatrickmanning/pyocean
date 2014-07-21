# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:10:22 2013

@author: jmanning
plots fvcom bottom depths vs usgs for specified region
hardcodes are in separate file called "fvcom_depths_ctl.py"
"""

from pylab import *
import matplotlib.tri as Tri
from mpl_toolkits.basemap import Basemap
import netCDF4
import numpy as np
from fvcom_depths_ctl import * #imports hardcode variables
import sys
sys.path.append('../modules')
from basemap import basemap_standard,basemap_usgs

#get FVCOM depths
url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?lon,lat,h,nv'
nc = netCDF4.Dataset(url)
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
h = nc.variables['h'][:]
# read connectivity array
nv = nc.variables['nv'][:].T - 1
# create a triangulation object, specifying the triangle connectivity array
tri = Tri.Triangulation(lon,lat, triangles=nv)

# plot depth using tricontourf
fig=plt.figure(figsize=(6,8))
ax1=fig.add_subplot(211)
basemap_standard([latrng[0],latrng[1]],[lonrng[0],lonrng[1]],[0.2])
cont_range.reverse()
tricontourf(tri,h*-1,list(np.array(cont_range)*-1))#contour range from fvcom_depth_ctl.py file
colorbar()
ylim(latrng)
xlim(lonrng)
plt.title('FVCOM GOM3 Depth (m)') 
plt.plot([-68.158,-67.327,-67.248],[44.127,44.485,44.487],'w*',markersize=10)#cases of bad depths in FVCOM
plt.show()

# now plot usgs depths for specified region
ax2=fig.add_subplot(212)
print 'Now running basemap_usgs'
basemap_usgs([latrng[0],latrng[1]],[lonrng[0],lonrng[1]],True,True,[0.2],list(np.array(cont_range)*-1),1)
plt.title('USGS GOM3_v1_0 Depth (m)')
plt.plot([-68.158,-67.327,-67.248],[44.127,44.485,44.487],'w*',markersize=10)#bad depths
plt.text(-68.32,44.21,'Cranberry Isles',style='italic')
plt.show()
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/'+urlname+'fvcom_vs_usgs_'+case+'.png')
plt.savefig('/net/nwebserver/epd/ocean/MainPage/modvsobs/figs/'+urlname+'fvcom_vs_usgs_'+case+'.eps')
