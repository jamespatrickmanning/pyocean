#!/usr/bin/python
import sys
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib 
from utilities import lat2str, lon2str

#give the path for ob2 to import pydap
sys.path.append("/usr/local/lib/python2.7/dist-packages/Pydap-3.0.1-py2.7.egg")
from pydap.client import open_url
#from mpl_toolkits.basemap import Basemap

def adjustFigAspect(fig,aspect=1/1.3):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize,ysize = fig.get_size_inches()
    minsize = min(xsize,ysize)
    xlim = .4*minsize/xsize
    ylim = .4*minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=.5-xlim,
                        right=.5+xlim,
                        bottom=.5-ylim,
                        top=.5+ylim)

################################################################################


##plot the basemap
#parallels_interval mean the interval of xaxis and yaxis,if parallels_interval=0.1 the min(lat)=40.15 max(lat)=40.35, the yaxis label will be 40.2, 40.3 
#lat,lon should be list, if lat just has one value, the format is: lat=[43.5]
# plot the coastline,river,boundary, but the coastline is not good
def basemap_standard(lat,lon,*parallels_interval):
    ## plot the coastline   
    #set up the map in a Equidistant Cylindrical projection
    #Note: See "oceanographic_python.doc" on how to download and install the 3rd party "Basemap" package
    from mpl_toolkits.basemap import Basemap
    m = Basemap(projection='cyl',llcrnrlat=min(lat)-0.01,urcrnrlat=max(lat)+0.01,llcrnrlon=min(lon)-0.01,urcrnrlon=max(lon)+0.01,resolution='i')#,fix_aspect=False)
  #  draw coastlines
    m.drawcoastlines()
    m.fillcontinents(color='grey')
    m.drawmapboundary()
    #draw major rivers
    m.drawrivers()
    if len(parallels_interval)<1:
        parallels_interval=1
        #draw parallels
        m.drawparallels(np.arange(int(min(lat)),int(max(lat))+1,float(parallels_interval)),linewidth=0,labels=[1,0,0,0],fmt=lat2str,dashes=[2,2])
        #draw meridians
        m.drawmeridians(np.arange(int(min(lon)),int(max(lon))+1,float(parallels_interval)),linewidth=0,labels=[0,0,0,1],fmt=lon2str,dashes=[2,2])     
    else:
        parallels_interval=parallels_interval[0]
        #draw parallels
        #m.drawparallels(np.arange(round(min(lat)-0.2,3),round(max(lat)+0.2,3),parallels_interval),labels=[1,0,0,0],fmt=lat2str,dashes=[2,2])
        #draw meridians
        #m.drawmeridians(np.arange(round(min(lon)-0.2,3),round(max(lon)+0.2,3),parallels_interval),labels=[0,0,0,1],fmt=lon2str,dashes=[2,2]) 
        m.drawparallels(np.arange(round(min(lat),2),round(max(lat),2),parallels_interval),labels=[1,0,0,0],fmt=lat2str,dashes=[2,2])
        #draw meridians
        m.drawmeridians(np.arange(round(min(lon),2),round(max(lon),2),parallels_interval),labels=[0,0,0,1],fmt=lon2str,dashes=[2,2]) 


def basemap_usgs(lat,lon,bathy):
    # plot the coastline and, if bathy is True, bathymetry is plotted
    # lat and lon can be any list of positions in decimal degrees

    url='http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v03'
    def get_index_latlon(url):# use the function to calculate the minlat,minlon,maxlat,maxlon location
        try:
          dataset=open_url(url)
        except:
          print "please check your url!"
          sys.exit(0)
        basemap_lat=dataset['lat']
        basemap_lon=dataset['lon']
        basemap_topo=dataset['topo']
    
        # add the detail of basemap
        minlat=min(lat)#-0.01
        maxlat=max(lat)#+0.01
        minlon=min(lon)#-0.01
        maxlon=max(lon)#+0.01
        index_minlat=int(round(np.interp(minlat,basemap_lat,range(0,basemap_lat.shape[0]))))
        index_maxlat=int(round(np.interp(maxlat,basemap_lat,range(0,basemap_lat.shape[0]))))

        index_minlon=int(round(np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        index_maxlon=int(round(np.interp(maxlon,basemap_lon,range(0,basemap_lon.shape[0]))))

        #print np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))
        #print index_minlon
        return index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo
    
    index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo = get_index_latlon(url)
    min_index_lat=min(index_minlat,index_maxlat)
    max_index_lat=max(index_minlat,index_maxlat)
    min_index_lon=min(index_minlon,index_maxlon)
    max_index_lon=max(index_minlon,index_maxlon)
    if index_maxlat-index_minlat==0 or index_maxlon-index_minlon==0:
        print "Using http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc"
        url='http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc'
        try:
          dataset=open_url(url)
        except:
          print "please check your url!"
          sys.exit(0)
        basemap_lat=dataset['lat']
        basemap_lon=dataset['lon']
        basemap_topo=dataset['topo']
        # add the detail of basemap
        minlat=min(lat)-0.01
        maxlat=max(lat)+0.01
        minlon=min(lon)-0.01
        maxlon=max(lon)+0.01
        basemap_lat=[float(i) for i in basemap_lat]
        basemap_lat_r=sorted(basemap_lat)
       # basemap_lat.reverse()
   
        range_basemap_lat=range(len(basemap_lat))
        range_basemap_lat.reverse()
        index_minlat=int(round(np.interp(minlat,basemap_lat_r,range_basemap_lat)))
        index_maxlat=int(round(np.interp(maxlat,basemap_lat_r,range_basemap_lat)))




        index_minlon=int(round(np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        index_maxlon=int(round(np.interp(maxlon,basemap_lon,range(0,basemap_lon.shape[0]))))

        # index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo = get_index_latlon(url)
        min_index_lat=min(index_minlat,index_maxlat)
        max_index_lat=max(index_minlat,index_maxlat)
        min_index_lon=min(index_minlon,index_maxlon)
        max_index_lon=max(index_minlon,index_maxlon) 
 
    #print "topo indexes: "+str(min_index_lat)+','+str(max_index_lat)+','+str(min_index_lon)+','+str(max_index_lon)
    X,Y=np.meshgrid(basemap_lon[min_index_lon:max_index_lon],basemap_lat[min_index_lat:max_index_lat])

    # You can set negative contours to be solid instead of dashed:
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    # plot the depth
    #print index_minlat,index_maxlat
    #plt.xlim([min(lon),max(lon)])
    #plt.ylim([min(lat),max(lat)])
    #plot the bathy
    if bathy==True:
        plt.contourf(X,Y,basemap_topo.topo[min_index_lat:max_index_lat,index_minlon:index_maxlon],[-30, -20, -10, 0],colors=['yellow','blue','green','cyan'],linewith=0.05)
        #plt.clabel(CS, fontsize=7,fmt='%5.0f', inline=1)
    #plt.clabel(cs, fontsize=9, inline=1,fmt='%5.0f'+"m")
    if min_index_lat==max_index_lat:
        print "No basemap_usgs data available for this area"
    #else:    
        #plt.contourf(X,Y,basemap_topo.topo[min_index_lat:max_index_lat,min_index_lon:max_index_lon],[0,1000],colors='grey')
    #plt.contourf(X,Y,basemap_topo.topo[min_index_lat:max_index_lat,min_index_lon:max_index_lon],[-90,-60],colors='black')


#parallels_interval mean the interval of xaxis and yaxis,if parallels_interval=0.1 the min(lat)=40.15 max(lat)=40.35, the yaxis label will be 40.2, 40.3 
#lat,lon should be list, if lat just has one value, the format is: lat=[43.5]
# get the coastline and depth value from the url, so can plot the detail of the coastline
def basemap_detail(lat,lon,bathy,draw_parallels,*parallels_interval):
    ## plot the coastline

    url='http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v03'
    def get_index_latlon(url):# use the function to calculate the minlat,minlon,maxlat,maxlon location
        try:
          dataset=open_url(url)
        except:
          print "please check your url!"
          sys.exit(0)
        basemap_lat=dataset['lat']
        basemap_lon=dataset['lon']
        basemap_topo=dataset['topo']
    
        # add the detail of basemap
        minlat=min(lat)-0.01
        maxlat=max(lat)+0.01
        minlon=min(lon)+0.01
        maxlon=max(lon)-0.01
        index_minlat=int(round(np.interp(minlat,basemap_lat,range(0,basemap_lat.shape[0]))))
        index_maxlat=int(round(np.interp(maxlat,basemap_lat,range(0,basemap_lat.shape[0]))))
        index_minlon=int(round(np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        index_maxlon=int(round(np.interp(maxlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        return index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo
    
    
    index_minlat,index_maxlat,index_minlon,index_maxlon,basemap_lat,basemap_lon,basemap_topo = get_index_latlon(url)
    #print index_minlat,index_maxlat,index_minlon,index_maxlon
    if index_minlat==0 or index_maxlat==0 or index_minlon==0 or index_maxlon==0:
        
        url='http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc'
        try:
          dataset=open_url(url)
        except:
          print "please check your url!"
        sys.exit(0)
        basemap_lat=dataset['lat']
        basemap_lon=dataset['lon']
        basemap_topo=dataset['topo']
        # add the detail of basemap
        minlat=min(lat)-0.01
        maxlat=max(lat)+0.01
        minlon=min(lon)+0.01
        maxlon=max(lon)-0.01
        basemap_lat=[float(i) for i in basemap_lat]
        basemap_lat.reverse()
        range_basemap_lat=range(len(basemap_lat))
        range_basemap_lat.reverse()
        index_minlat=int(round(np.interp(minlat,basemap_lat,range_basemap_lat)))
        index_maxlat=int(round(np.interp(maxlat,basemap_lat,range_basemap_lat)))
        index_minlon=int(round(np.interp(minlon,basemap_lon,range(0,basemap_lon.shape[0]))))
        index_maxlon=int(round(np.interp(maxlon,basemap_lon,range(0,basemap_lon.shape[0]))))
    min_index_lat=min(index_minlat,index_maxlat)
    max_index_lat=max(index_minlat,index_maxlat)
    X,Y=np.meshgrid(basemap_lon[index_minlon-15:index_maxlon+15],basemap_lat[min_index_lat-15:max_index_lat+15])

    # You can set negative contours to be solid instead of dashed:
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    #plot the bathy
    if bathy==True:
        CS=plt.contour(X,Y,basemap_topo.topo[min_index_lat-15:max_index_lat+15,index_minlon-15:index_maxlon+15],3,colors='gray',linewith=0.05)
        plt.clabel(CS, fontsize=7,fmt='%5.0f', inline=1)
    #plt.clabel(cs, fontsize=9, inline=1,fmt='%5.0f'+"m")
    plt.contourf(X,Y,basemap_topo.topo[min_index_lat-15:max_index_lat+15,index_minlon-15:index_maxlon+15],[0,1000],colors='grey')
    ax=plt.gca()
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    
    #set up the map in a Equidistant Cylindrical projection
    #m.drawmapboundary()
    #draw major rivers
    #m.drawrivers()
    if draw_parallels==True:
        
      from mpl_toolkits.basemap import Basemap
      m = Basemap(projection='cyl',llcrnrlat=min(lat),urcrnrlat=max(lat),\
          llcrnrlon=min(lon),urcrnrlon=max(lon),resolution='h',suppress_ticks=False)#,fix_aspect=False)
      if len(parallels_interval)<1:
        parallels_interval=1
        #draw parallels     
        m.drawparallels(np.arange(int(min(lat)),int(max(lat)),float(parallels_interval)),labels=[1,0,0,0],fmt=lat2str,dashes=[2,2])
        #draw meridians
        m.drawmeridians(np.arange(int(min(lon)),int(max(lon)),float(parallels_interval)),labels=[0,0,0,1],fmt=lon2str,dashes=[2,2])     
      else:
        parallels_interval=parallels_interval[0]
        #draw parallels
        m.drawparallels(np.arange(round(min(lat),3),round(max(lat),3),parallels_interval),labels=[1,0,0,0],fmt=lat2str,dashes=[2,2])
        #draw meridians
        m.drawmeridians(np.arange(round(min(lon),3),round(max(lon),3),parallels_interval),labels=[0,0,0,1],fmt=lon2str,dashes=[2,2]) 

def basemap_region(region):
    path="" # Y:/bathy/"#give the path if these data files are store elsewhere
    #if give the region, choose the filename
    if region=='sne':
        filename='/net/data5/jmanning/bathy/sne_coast.dat'
    if region=='cc':
        filename='/net/data5/jmanning/bathy/capecod_outline.dat'
    if region=='bh':
        filename='/net/data5/jmanning/bathy/bostonharbor_coast.dat'
    if region=='cb':
        filename='cascobay_coast.dat'
    if region=='pb':
        filename='penbay_coast.dat'
    
    #open the data
    f=open(path+filename)

    lon,lat=[],[]
    for line in f:#read the lat, lon
	    lon.append(line.split()[0])
	    lat.append(line.split()[1])
    nan_location=[]
    # plot the lat,lon between the "nan"
    for i in range(len(lon)):#find "nan" location
        if lon[i]=="nan":
            nan_location.append(i)

    for m in range(1,len(nan_location)):#plot the lat,lon between nan
        lon_plot,lat_plot=[],[]
        for k in range(nan_location[m-1],nan_location[m]):
            lat_plot.append(lat[k])
            lon_plot.append(lon[k])
        plt.plot(lon_plot,lat_plot,'r') 
