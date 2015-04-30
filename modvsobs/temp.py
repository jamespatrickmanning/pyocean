# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:19:22 2015

@author: jmanning
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import float64
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd
import pytz
import sys
import netCDF4
from matplotlib import path
from dateutil import rrule
# import our local modules
sys.path.append('../modules')
from getdata import getemolt_latlon,getobs_tempsalt
#sys.path.append('../../roms')
import jmath,jata
from conversions import dm2dd,f2c
from utilities import my_x_axis_format
def bbox2ij(lons, lats, bbox):
    bbox = np.array(bbox)
    mypath = np.array([bbox[[0,1,1,0]],bbox[[2,2,3,3]]]).T
    p = path.Path(mypath)
    points = np.vstack((lons.flatten(),lats.flatten())).T
    tshape = np.shape(lons)
    inside = []
    for i in range(len(points)):
        inside.append(p.contains_point(points[i]))
    inside = np.array(inside, dtype=bool).reshape(tshape)
    index = np.where(inside==True)
    if not index[0].tolist():          # bbox covers no area
        raise Exception('no points in this area')
    else:
        return index
def nearest_point_index( lon, lat, lons, lats, length=(1, 1)):
    bbox = [lon-length[0], lon+length[0], lat-length[1], lat+length[1]]
    index = bbox2ij(lons, lats, bbox)
    lon_covered = lons[index]
    lat_covered = lats[index]
    cp = np.cos(lat_covered*np.pi/180.)
    dx = (lon-lon_covered)*cp
    dy = lat-lat_covered
    dist = dx*dx+dy*dy
    mindist = np.argmin(dist)
    indx = [i[mindist] for i in index]
    return indx, dist[mindist]