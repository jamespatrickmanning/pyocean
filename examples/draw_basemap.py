import sys
sys.path.append("../modules")
import basemap as bm
import matplotlib.pyplot as plt

# the following three lines are needed to later place the figure windows on the screen
import matplotlib
matplotlib.use("wx")

import pylab

# use the standard Basemap
plt.figure(1,figsize=(5,4)) # makes figure less than the defaul 8x6 inches
bm.basemap_standard([42.0,43.0],[-71.,-70.0],[0.5]) # always make this last argument a list in brackets
# position figure window on the screen
thismanager1 = pylab.get_current_fig_manager()
thismanager1.window.SetPosition((0, 0))
plt.title('basemap_standard')
plt.show()

# use the ascii files of coastline already on disk
plt.figure(2,figsize=(5,4))
bm.basemap_region('sne')
thismanager2 = pylab.get_current_fig_manager()
thismanager2.window.SetPosition((0, 500))
plt.title('basemap_region')
plt.show()

# extract coastline and bathymetry using pydap
plt.figure(3,figsize=(5,4))
bm.basemap_usgs([42.0,43.0],[-71.,-70.0],True,True,[0.5],[-50,0],5)
thismanager3 = pylab.get_current_fig_manager()
thismanager3.window.SetPosition((500, 0))
plt.title('basemap_usgs')
plt.show()


# extract coastline and bathymetry using pydap
plt.figure(4,figsize=(5,4))
bm.basemap_detail([40.0,43.0],[-71.,-65.0],True,True,0.5)
thismanager4 = pylab.get_current_fig_manager()
thismanager4.window.SetPosition((500, 500))
plt.title('basemap_detail')
plt.show()


