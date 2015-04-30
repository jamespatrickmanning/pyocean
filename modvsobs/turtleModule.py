from datetime import datetime, timedelta
import numpy as np
from mpl_toolkits.basemap import Basemap
from math import sqrt 
import pandas as pd
def mon_alpha2num(m):
    '''
    Return num from name of Month
    '''
    month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    if m in month:
        n = month.index(m)
    else:
        raise Exception('Wrong month abbreviation')
    return n+1
def np_datetime(m):
    if type(m) is str:
        year = int(m[5:9])
        month = mon_alpha2num(m[2:5])
        day =  int(m[0:2])
        hour = int(m[10:12])
        minute = int(m[13:15])
        second = int(m[-2:])
        dt = datetime(year,month,day,hour=hour,minute=minute,second=second)
    else:
        dt = []
        for i in m:
            year = int(i[5:9])
            month = mon_alpha2num(i[2:5])
            day =  int(i[0:2])
            hour = int(i[10:12])
            minute = int(i[13:15])
            second = int(i[-2:])
            temp = datetime(year,month,day,hour=hour,minute=minute,second=second)
            dt.append(temp)
        dt = np.array(dt)
    return dt
def mean_value(v):
    '''
    return the mean value from ctd observation 'TEMP_VALS'
    '''
    v_list = []
    for i in v:
        print i, type(i)
        l = i.split(',')
        val = [float(i) for i in l]
        v_mean = np.mean(val)
        v_list.append(v_mean)
    return v_list
def bottom_value(v):
    '''
    return the bottom temp from observation 'TEMP_VALS' str
    '''
    v_list = []
    for i in v:
        l = i.split(',')
        val = float(l[-1])
        v_list.append(val)
    v_list = np.array(v_list)
    return v_list
def index_by_depth(v, depth):
    '''
    v should be a list of ocean depth
    Return a list with 2 part divided by 'depth'
    '''
    i = {}
    i[0] = v[v<depth].index
    i[1] = v[v>=depth].index
    return i
def str2list(s, bracket=False):
    '''
    a is a string converted from a list
    a = '[3,5,6,7,8]'
    b = str2list(a, bracket=True)
    or
    a = '3,4,5,6'
    b = str2list(a)
    '''
    if bracket:
        s = s[1:-1]
    s = s.split(',')
    s = [float(i) for i in s]
    return s
def str2ndlist(arg, bracket=False):
    '''
    convert list full of str to multidimensional arrays
    '''
    ret = []
    for i in arg:
        a = str2list(i, bracket=bracket)
        ret.append(a)
    # ret = np.array(ret)
    return ret
def angle_conversion(a):
    a = np.array(a)
    return a/180*np.pi
def dist(lon1, lat1, lon2, lat2):
    R = 6371.004
    lon1, lat1 = angle_conversion(lon1), angle_conversion(lat1)
    lon2, lat2 = angle_conversion(lon2), angle_conversion(lat2)
    l = R*np.arccos(np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2)+\
                        np.sin(lat1)*np.sin(lat2))
    return l
def closest_num(num, numlist, i=0):
    '''
    Return index of the closest number in the list
    '''
    index1, index2 = 0, len(numlist)
    indx = int(index2/2)
    if not numlist[0] < num < numlist[-1]:
        raise Exception('{0} is not in {1}'.format(str(num), str(numlist)))
    if index2 == 2:
        l1, l2 = num-numlist[0], numlist[-1]-num
        if l1 < l2:
            i = i
        else:
            i = i+1
    elif num == numlist[indx]:
        i = i + indx
    elif num > numlist[indx]:
        i = closest_num(num, numlist[indx:],
                          i=i+indx)
    elif num < numlist[indx]:
        i = closest_num(num, numlist[0:indx+1], i=i)
    return i
def draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2):
    ax = fig.sca(ax)
    dmap = Basemap(projection='cyl',
                   llcrnrlat=min(latsize)-0.01,
                   urcrnrlat=max(latsize)+0.01,
                   llcrnrlon=min(lonsize)-0.01,
                   urcrnrlon=max(lonsize)+0.01,
                   resolution='h',ax=ax)
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0], linewidth=0,fontsize=20)
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1], linewidth=0,fontsize=20)
    dmap.drawcoastlines()
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()
def intersection(l1, l2):
    '''
    Calculate point of intersection of two lines.
    line1: y = k1*x + b1
    line2: y = k2*x + b2
    x, y = intersection((k1, b1), (k2, b2))
    '''
    k1, b1 = l1[0], l1[1]
    k2, b2 = l2[0], l2[1]
    x = (b2-b1)/(k1-k2)
    y = k1*x + b1
    return x, y
def whichArea(arg, lst):
    #Calculate certain point belongs to which area.
    i = len(lst)//2
    if i != 0: 
        if arg >= lst[i]:
            r = i + whichArea(arg, lst[i:])
        elif arg < lst[i]:
            r = whichArea(arg, lst[:i])
    else: r = i
    return r    
def point_dist(x0,y0,x1,y1,x2,y2):
    k=(y1-y2)/(x1-x2)
    l=abs(k*(x0-x1)-(y0-y1))/sqrt(1+k*k)
    return l
def get_centerdepth(x,y,dx1,dx2,dy1,dy2):
    a=x+y    
    n=dx1*x/a+dx2*y/a
    m=dy1*x/a+dy2*y/a
    d=n*x/a+m*y/a
    return d
def get_all_depth(obsLons,obsLats,modLons,modLats,moddepth,modNearestIndex):
    depth=[]
    I=[]
    for i in obsLons.index:
        I.append(i)
        dist=[]
        if modNearestIndex[i][1]<129:
            dist.append(point_dist(obsLons[i],obsLats[i],modLons[modNearestIndex[i][0]][modNearestIndex[i][1]],modLats[modNearestIndex[i][0]][modNearestIndex[i][1]],
                   modLons[modNearestIndex[i][0]][modNearestIndex[i][1]+1],modLats[modNearestIndex[i][0]][modNearestIndex[i][1]]))
            dist.append(point_dist(obsLons[i],obsLats[i],modLons[modNearestIndex[i][0]][modNearestIndex[i][1]],modLats[modNearestIndex[i][0]][modNearestIndex[i][1]+1],
                   modLons[modNearestIndex[i][0]][modNearestIndex[i][1]+1],modLats[modNearestIndex[i][0]][modNearestIndex[i][1]+1]))
            depth.append(get_centerdepth(dist[0],dist[1],moddepth[modNearestIndex[i][0]][modNearestIndex[i][1]],moddepth[modNearestIndex[i][0]+1][modNearestIndex[i][1]],
                   moddepth[modNearestIndex[i][0]][modNearestIndex[i][1]+1],moddepth[modNearestIndex[i][0]+1][modNearestIndex[i][1]+1]))
        if modNearestIndex[i][1]==129:
            depth.append(moddepth[modNearestIndex[i][0]][modNearestIndex[i][1]])
    return depth
def colors(n):
    """Compute a list of distinct colors, each of which is represented as an RGB 3-tuple."""
    """It's useful for less than 100 numbers"""
    if pow(n,float(1)/3)%1==0.0:
        n+=1 
	  #make sure number we get is more than we need.
    rgbcolors=[]
    x=pow(n,float(1)/3)
    a=int(x)
    b=int(x)
    c=int(x)
    if a*b*c<=n:
       a+=1
    if a*b*c<n:
       b+=1
    if a*b*c<n:
       c+=1
    for i in range(a):
       r=0.99/(a)*(i)
       for j in range(b):
          s=0.99/(b)*(j)
          for k in range(c):
             t=0.99/(c)*(k)
             color=r,s,t
             rgbcolors.append(color)
    return rgbcolors
def np_datetimes(m):
    'change shipdata time to datetime'
    dt = []
    for i in m:
        year = int(i[8:12])
        month = mon_alpha2num(i[4:7])
        day =  int(i[1:3])
        temp = datetime(year,month,day)
        dt.append(temp)
    dt = np.array(dt)
    return dt
