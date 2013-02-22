"""
Compares eMOLT with FVCOM bottom temp
@author: jmanning, rsignell, yacheng
"""
import matplotlib.pyplot as plt
import netCDF4
from getdata import getemolt_latlon,getemolt_temp
from conversions import dm2dd,f2c
from utilities import nearxy

site='BN01'
[lati,loni,on]=getemolt_latlon(site) # extracts lat/lon based on site code
[lati,loni]=dm2dd(lati,loni) #converts decimal-minutes to decimal degrees
[obs_dt,obs_temp]=getemolt_temp(site) # extracts time series
for kk in range(len(obs_temp)):
  obs_temp[kk]=f2c(obs_temp[kk]) # converts to Celcius

# now get the model output
urlfvcom = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
nc = netCDF4.Dataset(urlfvcom)
nc.variables
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
times = nc.variables['time']
jd = netCDF4.num2date(times[:],times.units)
vname = 'temp'
var = nc.variables[vname]

# find nearest point to desired location and time
inode = nearxy(lon,lat,loni,lati)
index=netCDF4.date2index([obs_dt[0],obs_dt[-1]],times,select='nearest')#find the model time index at start & end pf obs

#plot them
fig=plt.figure(figsize=(16,4))
ax=fig.add_subplot(111)
ax.plot_date(obs_dt,obs_temp,fmt='-')
plt.grid()
ax.plot_date(jd[index[0]:index[1]],var[index[0]:index[1],44,inode],fmt='-',color='red')
plt.ylabel(var.units)
plt.title('eMOLT site '+site+' temp vs FVCOM '+'%s at node=%d (Lon=%.4f, Lat=%.4f)' % (vname, inode+1, lon[inode], lat[inode]))
plt.legend(['observed','modeled'],loc='best')
plt.show()