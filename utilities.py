# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:40:30 2012
This is a collection of code I found outside normal Python distribution
that does a variety of things. For example, the "smooth" function below
does filtering better than I could find in the python moving average functions
@author: jmanning
"""

import numpy as np
import math

def choose_date_label(start,end):
    from datetime import timedelta as td
    import matplotlib.dates as mdates
    #delta = num2date(end) - num2date(start)
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
  a=axis_object.get_xlim()
  loc,fmt=choose_date_label(a[0],a[1])# calls another function within this module
  axis_object.xaxis.set_minor_formatter(fmt)
  axis_object.xaxis.set_minor_locator(loc)

####### lat2str, lon2str is the function used for while drawing parallels, give the format for axis.
####### used in draw basemap: draw parallels
def lat2str(deg):
    min = 60 * (deg - np.floor(deg))
    deg = np.floor(deg)
    dir = 'N'
    if deg < 0:
        if min != 0.0:
            deg += 1.0
            min -= 60.0
        dir = 'S'
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
    return (u"%d\N{DEGREE SIGN} %g' %s") % (np.abs(deg),np.abs(min),dir)

# function to find index to nearest point    
def nearxy(y_array, x_array, y_point, x_point):
    distance = (y_array-y_point)**2 + (x_array-x_point)**2
    idy = np.where(distance==distance.min())
    return idy[0]

def nearxy_old(x,y,x0,y0):#includes min distance
  distance=[]
  for i in range(0,len(x)):   
    distance.append(abs(math.sqrt((x[i]-x0)**2+(y[i]-y0)**2)))
  min_dis=min(distance)
  len_dis=len(distance)
  index=[]
  for ii in range(0,len_dis):
    if distance[ii]==min_dis:
      index.append(ii)
  return min(distance),index[0]

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


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def uniquecolors(n):
    """Compute a list of distinct colors, each of which is represented as an RGB 3-tuple."""
    hues = []
    # i is in the range 0, 1, ..., n - 1
    for i in range(1,n):
        hues.append(360.0 / i)

    hs = []
    for hue in hues:
        h = math.floor(hue / 60) % 6
        hs.append(h)

    fs = []
    for hue in hues:
        f = hue / 60 - math.floor(hue / 60)
        fs.append(f)

    rgbcolors = []
    for h, f in zip(hs, fs):
        v = 1
        p = 0
        q = 1 - f
        t = f
        if h == 0:
            color = v, t, p
        elif h == 1:
            color = q, v, p
        elif h == 2:
            color = p, v, t
        elif h == 3:
            color = p, q, v
        elif h == 4:
            color = t, p, v
        elif h == 5:
            color = v, p, q
        rgbcolors.append(color)

    return rgbcolors    


