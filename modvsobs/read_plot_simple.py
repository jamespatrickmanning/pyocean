import pandas as pd
from matplotlib import pyplot as plt

# read drifter track and plot it
cols=['ID','ESN','MTH','DAY','HR_GMT','MIN','YEARDAY','LON','LAT','DEPTH','TEMP']
df=pd.read_csv('http://nefsc.noaa.gov/drifter/drift_cscr_2014_1.dat',delim_whitespace=True,names=cols)
plt.plot(df['LON'],df['LAT'])
plt.show()

# Now, add some coastline (assuming you have the coastline on line)
coast=pd.read_csv('/net/data5/jmanning/bathy/necscoast_worldvec.dat',delim_whitespace=True)
plt.plot(coast.lon,coast.lat)
