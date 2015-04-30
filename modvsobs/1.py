import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import netCDF4
from matplotlib.mlab import griddata
import sys
sys.path.append('../modules')
import basemap
from basemap import basemap_usgs,basemap_standard
from turtleModule import dist,str2ndlist
lat_AB01=42.0368
lon_AB01=-70.1313
lat=np.arange(41.7797,42.0368,0.025)
lon=np.arange(-70.4873,-70.0,0.035)
time=[datetime(2004,9,17),datetime(2004,9,27)]
distance_AB01=dist(lon[0],lat[0],lon_AB01,lat_AB01)
deepest=[14.6066,27.6068,27.792999,31.504299,34.486198,36.026402,37.494999,38.680599,
                                         40.936199,35.314899,25.784]
fig=plt.figure()
ax=fig.add_subplot(111)
distance=list(np.array([dist(lon[0],lat[0],lon[-1],lat[-1])])/len(lat)*range(1,len(lat)+1))
polygon=[]
for j in range(len(deepest)):
   polygon.append([distance[j],deepest[j]])
polygon.append([distance[-1],max(deepest)+1])
polygon.append([distance[0],max(deepest)+1])
plt.ylim([max(deepest)+1,0])
plt.xlim([min(distance),max(distance)])
pg=plt.Polygon(polygon,color='red')  
ax.add_patch(pg)
plt.show()