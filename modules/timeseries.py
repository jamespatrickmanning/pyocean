import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.dates import DateFormatter
from matplotlib.dates import num2date
from matplotlib.dates import RRuleLocator
from conversions import uv2sd
import numpy as np


def plot_uv(time,u,v):
    "plot u,v,time"
    fig=plt.figure()
    fig.canvas.set_window_title('time u&v')
    ax = fig.add_subplot(111)
    ax.plot(time,u,'-',label='u')
    ax.plot(time,v,'-',label='v')
    plt.legend()
    #locator = mpl.dates.AutoDateLocator()
    #formatter =mpl.dates.AutoDateFormatter()
    #formatter.scaled[1/(24)]
    #locator.intervald[HOURLY] = [3]
    #ax.xaxis.set_major_locator(locator)
    monthsFmt = DateFormatter('%m-%d %H'+'h')
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.set_xlabel(num2date(time[0]).year,fontsize=17)
    plt.show()
    
def plot_sd(time,u,v):
    "convert u&v to s&d,and plot them"
    print u
    print v
    z=zip(u,v)
    s,d=[],[]
    for i in range(0,np.size(z)/2):
        u[i]=z[i][0]
        v[i]=z[i][1]
        (s1,d1)=uv2sd(u[i],v[i])
        s.append(s1)
        d.append(d1)
    fig=plt.figure()
    fig.canvas.set_window_title('time s&d')
    ax = fig.add_subplot(111)
    ax.plot(time,s,'-',label='s')
    ax.plot(time,d,'-',label='d')
    plt.legend()
    locator = mpl.dates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    monthsFmt = DateFormatter('%m-%d %H'+'h')
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.set_xlabel(num2date(time[0]).year,fontsize=17)
    plt.show()
    
      
    
