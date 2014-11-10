''' 
This routine compares MULTIPLE drifter tracks to MULTIPLE model-derived tracks
It is a enhanced version of Jian's track_cmp.py routine as modified by Conner Warren in summer 2014.
Many of the functions and variables were renamed to better reflect their tasks and identity. 
Some comments and adjustments by JiM and Bingwei.
In November 2014, we added the option to run the code backwards

GENERAL NOTES:
    1. Hardcodes are at the beginning of the program or function
    2. If any major changes are made, the flowcharts MUST be updated
'''

#Step 1: Import modules
import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta
from matplotlib import path
import calendar
import pytz
import pandas as pd
sys.path.append('../bin')
import netCDF4 
from track_functions import get_drifter, get_fvcom, get_roms, draw_basemap, distance # all homegrown functions needed for this routine
from makegrid import clickmap, points_between

########## Step 2: Hardcode constants ###########################
# Three options to define track start 1) by drifters,  2) user defined along a straight line(s), 3) clicking map
option=3
numpts=7 # needed for case where option==3
#starttime = None             # If it's None, use the last drifter time.
starttime =  datetime(2013,6,10,12,0,0,0,pytz.UTC) # when "DIREC" is backwards "endtime" will be BEFORE starttime
endtime = datetime(2013,6,20,14,0,0,0,pytz.UTC)
DIREC='forwards' #'backwards' or 'forwards'
MODE = 'HINDCAST'            # 'FORECAST' or 'HINDCAST'
INPUT_DATA = 'drift_X.dat'   # if raw data, use "drift_X.dat";if want to get drifter data in database, use "None" 
DEPTH = -1.                  # depth of drogue in meters
DAYS = 1                     # Number or None. Length of time wanted in track, if not given, track to the last poistion of drifter.
MODEL = 'FVCOM'               # 'FVCOM', 'ROMS' or 'BOTH'
GRID = 'massbaya'                # '30yr', 'massbaya', 'GOM3a', 'GOM3' or 'massbay'(where both 'GOM3' and 'massbay' are forecast), only used in fvcom.
OUTPUTDIR='/net/nwebserver/epd/ocean/MainPage/track/ccbay/'
##################  END OF HARCODE SECTION ######################

if option==1: # specified drifters
   drifter_ids = ['115410701','118410701','108410712','108420701','110410711','110410712','110410713','110410714',
               '110410715','110410716','114410701','115410701','115410702','119410714','135410701','110410713','119410716']                                                  # Default drifter ID
elif option==2: # user specified pts
   [lat,lon]=points_between([42.501167, 41.801167],[-70.529587,-70.529587],3)# lat & lon in mid-Cape Cod Bay only needed when drift_id=0 (ie no drifter available)
   [lat2,lon2]=points_between([42.501167, 42.501167],[-70.529587,-70.129587],3)
   lat=lat+lat2
   lon=lon+lon2
   drifter_ids = range(len(lat))  # if <100, no drifter ...
elif option==3: # click on a map
   [lon,lat]=clickmap(numpts) # gets lat/lon by clicking map
   drifter_ids=range(len(lat))

for ID in drifter_ids:
    print "ID: ", ID
    if ID>100:
       drifter = get_drifter(ID, INPUT_DATA)# New drifter data or old drifter data
       points_drifter = drifter.get_track(starttime,DAYS)
    else:
       print 'starting at '+str(lat[ID])+' '+str(lon[ID])+' for '+str((endtime-starttime).days)+' days'
    if MODE == 'HINDCAST':
        #if MODEL in ("FVCOM", "BOTH"):
        #    assert GRID=="30yr"
        if ID>100:
          starttime = points_drifter['time'][0]
          endtime = points_drifter['time'][-1]
          lon, lat = points_drifter['lon'][0], points_drifter['lat'][0]

    elif MODE == 'FORECAST':
        # adjust for the added 4 hours in the models
        time1 = pytz.utc.localize(datetime.now().replace(hour=0,minute=0))-timedelta(days=3)
        # get starttime, and lon, lat
        if starttime:
            if starttime < time1:
                raise Exception('start time should be later than the time that 3days before today.')
            l1 = points_drifter['time']-points_drifter['time'][0]
            l2 = starttime - points_drifter['time'][0]
            index = np.where(abs(l1-l2)==min(abs(l1-l2)))[0][0]
            lon, lat = points_drifter['lon'][index], points_drifter['lat'][index]
        else:
            starttime = points_drifter['time'][-1]
            if starttime < time1:
                raise Exception('starttime should be later than the time that 3days before today, drifter is too old')
            lon, lat = points_drifter['lon'][-1], points_drifter['lat'][-1]
        # get endtime
        if DAYS:
            endtime = starttime + timedelta(days=DAYS)
        else:
            endtime = starttime + timedelta(days=3)
    # read data points from fvcom and roms websites and store them

    #set latitude and longitude arrays for basemap
    if ID>100:
      lonsize = [min(points_drifter['lon']), max(points_drifter['lon'])]
      latsize = [min(points_drifter['lat']), max(points_drifter['lat'])]
      diff_lon = (lonsize[0]-lonsize[1])/4. # leave space in sides
      diff_lat = (latsize[1]-latsize[0])/4.
    else:
       lonsize = [lon[ID],lon[ID]]
       latsize  = [lat[ID],lat[ID]]
       diff_lon =0.5
       diff_lat=0.5
    lonsize = [lonsize[0]-diff_lon,lonsize[1]+diff_lon]
    latsize = [latsize[0]-diff_lat,latsize[1]+diff_lat]
    if (ID==0) | (ID>100): # case of multiple start positions specified
       fig = plt.figure()
       ax = fig.add_subplot(111)
       draw_basemap(fig, ax, lonsize, latsize)
    if ID > 100:
      ax.plot(points_drifter['lon'],points_drifter['lat'],'ro-',label='drifter')
      ax.plot(points_drifter['lon'][0],points_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
    else:
      ax.plot(lon[ID],lat[ID],'g.',markersize=20)
      if ID==0:
         ax.annotate('Start', xy=(lon[ID], lat[ID]), xytext=(lon[ID]+0.02, lat[ID]+0.02),arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc,angleA=0,armA=30,rad=10",facecolor='black'))
    if MODEL in ('FVCOM', 'BOTH'):
        get_fvcom_obj = get_fvcom(GRID)
        url_fvcom = get_fvcom_obj.get_url(starttime, endtime)
        points_fvcom = get_fvcom_obj.get_track(lon[ID],lat[ID],DEPTH,url_fvcom)           # iterates fvcom's data
        #dist_fvcom = distance((points_drifter['lat'][-1],points_drifter['lon'][-1]),(points_fvcom['lat'][-1],points_fvcom['lon'][-1]))
        dist_fvcom = distance((lat[ID],lon[ID]),(points_fvcom['lat'][-1],points_fvcom['lon'][-1]))
        print 'The separation of fvcom was %f kilometers for drifter %s' % (dist_fvcom[0], ID )
        ax.plot(points_fvcom['lon'],points_fvcom['lat'],'ro-',label='fvcom')
    if MODEL in ('ROMS', 'BOTH'):
        get_roms_obj = get_roms()
        url_roms = get_roms_obj.get_url(starttime, endtime)
        points_roms = get_roms_obj.get_track(lon, lat, DEPTH, url_roms)
        if type(points_roms['lat']) == np.float64:                             # ensures that the single point case still functions properly   
            points_roms['lon'] = [points_roms['lon']] 
            points_roms['lat'] = [points_roms['lat']]
        #Calculate the distance separation
        dist_roms = distance((points_drifter['lat'][-1],points_drifter['lon'][-1]),(points_roms['lat'][-1],points_roms['lon'][-1]))
        print 'The separation of roms was %f kilometers for drifter %s' % (dist_roms[0], ID)
        ax.plot(points_roms['lon'],points_roms['lat'], 'go-', label='roms')

if ID >100:
      plt.title('ID: {0}, {1} to {2}'.format(ID, starttime.strftime("%m/%d/%Y %H:%M"), endtime.strftime("%m/%d/%Y %H:%M")))
else:
      plt.title('{1} to {2}'.format(ID, starttime.strftime("%m/%d/%Y %H:%M"), endtime.strftime("%m/%d/%Y %H:%M")))
#plt.legend(loc='lower right')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
# plt.savefig('plots/'+MODEL+str(ID)+'.png')
plt.savefig(OUTPUTDIR+'ID-' + str(ID) +'-'+MODE+'-'+GRID+'.png')
