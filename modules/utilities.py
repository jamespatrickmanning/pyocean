
"""
Created on Thu Jan  5 14:40:30 2012
This is a collection of code I found outside normal Python distribution
that does a variety of things. For example, the "smooth" function below
does filtering better than I could find in the python moving average functions
@author: jmanning
"""

import numpy as np
import math
from datetime import timedelta as td
import matplotlib.dates as mdates
import colorsys

def choose_date_label(start,end):
          
    delta = end - start
    if delta <= td(minutes=10):
        loc = mdates.MinuteLocator()
        fmt = mdates.DateFormatter('%I:%M %p')
    elif delta <= td(minutes=30):
        loc = mdates.MinuteLocator(byminute=range(0,60,5))
        fmt = mdates.DateFormatter('%I:%M %p')
    elif delta <= td(hours=1):
        loc = mdates.MinuteLocator(byminute=range(0,60,15))
        fmt = mdates.DateFormatter('%I:%M %p')
    elif delta <= td(hours=6):
        loc = mdates.HourLocator()
        fmt = mdates.DateFormatter('%I:%M %p')
    elif delta <= td(days=1):
        loc = mdates.HourLocator(byhour=range(0,24,3))
        fmt = mdates.DateFormatter('%I:%M %p')
    elif delta <= td(days=3):
        loc = mdates.HourLocator(byhour=range(0,24,6))
        fmt = mdates.DateFormatter('%I:%M %p')
    elif delta <= td(weeks=2):
        loc = mdates.DayLocator()
        fmt = mdates.DateFormatter('%b %d')
    elif delta <= td(weeks=12):
        loc = mdates.WeekdayLocator()
        fmt = mdates.DateFormatter('%b %d')
    elif delta <= td(weeks=52):
        loc = mdates.MonthLocator()
        fmt = mdates.DateFormatter('%b')
    else:
        loc = mdates.MonthLocator(interval=3)
        fmt = mdates.DateFormatter('%b %Y')
    return loc,fmt

def fixticks(axis_object):
    print 'New2'  
    a = axis_object.get_xlim()
    loc,fmt = choose_date_label(a[0],a[1])
    axis_object.xaxis.set_minor_formatter(fmt)
    axis_object.xaxis.set_minor_locator(loc)


def lat2str(deg):
    min = 60 * (deg - np.floor(deg))
    deg = np.floor(deg)
    dir = 'N'
    if deg < 0:
        if min != 0.0:
            deg += 1.0
            min -= 60.0
        dir = 'S'
    if np.floor(min)==0:        
      return (u"%d\N{DEGREE SIGN}%s") % (np.abs(deg),dir)
    else:  
      return (u"%d\N{DEGREE SIGN} %g' %s") % (np.abs(deg),np.abs(min),dir)
  
def lon2str(deg):
    min = 60 * (deg - np.floor(deg))
    deg = np.floor(deg)
    dir = 'E'
    if deg < 0:
        if min != 0.0:
            deg += 1.0
            min -= 60.0
        dir = 'W'
    if np.floor(min)==0:        
      return (u"%d\N{DEGREE SIGN}%s") % (np.abs(deg),dir)
    else:  
      return (u"%d\N{DEGREE SIGN} %g' %s") % (np.abs(deg),np.abs(min),dir)

def my_x_axis_format(ax, dt):
           if dt>td(days=6):
                intr=int(dt.days/6)
           else:
                intr=2
    #ax.xaxis.set_minor_locator(dates.WeekdayLocator(byweekday=(1),interval=intr))
           ax.xaxis.set_minor_locator(mdates.DayLocator(interval=intr))
           ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b%d'))
           years= mdates.YearLocator() # every year
           yearsFmt = mdates.DateFormatter('')
           ax.xaxis.set_major_locator(years)
           ax.xaxis.set_major_formatter(yearsFmt)
           return ax
      
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

def nearxy(x,y,xp,yp):
    """
    i,min_dist=nearxy(x,y,xp,yp)
    find the closest node in the array (x,y) to a point (xp,yp)
    input:
        x,y - np.arrays of the grid nodes, cartesian coordinates
        xp,yp - point on a plane
        output:
            i - index of the closest node
            min_dist - the distance to the closest node
            For coordinates on a sphere use function nearlonlat
            
            Vitalii Sheremet, FATE Project
    """
    dx=x-xp
    dy=y-yp
    dist2=dx*dx+dy*dy
# dist1=np.abs(dx)+np.abs(dy)
    i=np.argmin(dist2)
    min_dist=np.sqrt(dist2[i])
    return i,min_dist
def nearxy_old(y_array, x_array, y_point, x_point):
    distance = (y_array-y_point)**2 + (x_array-x_point)**2
    idy = np.where(distance==distance.min())
    return idy[0]

def nearxy2(x,y,x0,y0): #returns both distance and index
   distance = []
   for i in range(0,len(x)):   
       distance.append(abs(math.sqrt((x[i]-x0)**2+(y[i]-y0)**2)))
   min_dis = min(distance)
   len_dis = len(distance)
   index = []
   for ii in range(0,len_dis):
       if distance[ii] == min_dis:
           index.append(ii)
   return min(distance),index[0]

def points_between(lat,lon,x):
    """ 
    For 2 positions, interpolate X number of points between them
    where "lat" and "lon" are two element list
    "x" is the number of points wanted between them
    returns lat0,lono
    """
    print lat
    lato=[]
    lono=[]
    lati=(lat[1]-lat[0])/float(x)
    loni=(lon[1]-lon[0])/float(x)
    for j in range(x):
        lato.append(lat[0]+lati*j)
        lono.append(lon[0]+loni*j)
    return lato,lono

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[x[window_len-1:0:-1], x, x[-1:-window_len:-1]]
    
    if window == 'flat': #moving average
        w = np.ones(window_len,'d')
    else:
        w = eval('numpy.'+ window +'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')
    return y


def uniquecolors(N):
    """
    Generate unique RGB colors
    input: number of RGB tuples to generate
    output: list of RGB tuples
    """
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    colors =  [colorsys.hsv_to_rgb(x*1.0/N, 0.5, 0.5) for x in range(N)]
    return colors
