import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import num2date,date2num
import datetime as dt
import matplotlib as mpl
import csv
import scipy
import conversions
from conversions import *




# plot lat,lon and show text at the location of day change    
def plot_latlon(lat,lon,dtime,id):
    # find places marking new day & annotate plot
    index_day=[]
    for i in range(1,np.size(dtime)):
      if dtime[i].day <> dtime[i-1].day:
          index_day.append(i-1)
    fig=plt.figure()
    plt.title('Drifter# '+str(id))
    ax = fig.add_subplot(111)
    plt.xlabel('Longitude W')
    plt.ylabel('Latitude N')
    plt.plot(lon,lat, color = 'blue', lw = 1)
    for i in index_day:
        ax.annotate(str(dtime[i].month)+"/"+str(dtime[i].day), xy=(lon[i], lat[i]),  xycoords='data',
                xytext=(10, 15), textcoords='offset points',
                arrowprops=dict(arrowstyle="->"))
    plt.show()

##read the csv file and get lat,lon,dt,jd
def read_drifter_file(filename):
    # This needed to be redone completely
    # time output needs to be in "datetime" form
    dataReader = csv.reader(open(filename,'rb'))
    verts=[]
    for row in dataReader:  
        if row[0][0] !='%':   #skip the command lines    
            verts.append(row)
        
    id,lat_num,lon_num,yearday=[],[],[],[]
    for vert in verts:
        lat_num.append(vert[0].split()[8]) #latitude
        lon_num.append(vert[0].split()[7]) #longtitude
        yearday.append(vert[0].split()[6]) #yearday
        id.append(vert[0].split()[0])
  
    yeartime="20"+id[0][0:2] #get the year frome the id
    lat_float=[float(i) for i in lat_num]
    lon=[float(i) for i in lon_num]
    lat=[]
    for lati in lat_float:
        lat.append(str(lati))
    #delete "nan" form lat
    lat_array=scipy.array(lat)#convert list to array
    lat_nan_list=list(np.nonzero(lat_array=='nan'))#get location of the 'nan'
    lat_nan_id=list(lat_nan_list[0])#convert dt_zero_list to list format
    lat_nan_id.reverse()# reverse the lat_nan_id
    for locationi in lat_nan_id:
        del lat[locationi],lon[locationi],yearday[locationi]#del the lines which lat="nan"

  
    yearday_number = [float(i) for i in yearday]
    dti = list(np.diff(yearday_number)*24*60*60)#convert yearday_difference to seconds
    dt = []
    for dti in dti:
        dt.append(str(dti))
  
    lat=[float(i) for i in lat]  #the lat is number for calculate and plot
    jd=[float(i) for i in yearday] #the lon is number for calculate and plot
    dt=[float(i) for i in dt]

    dt_zero=scipy.array(dt)#convert list to array
    dt_zero_list=list(np.nonzero(dt_zero==0.0))#get location of the 0.0
    dt_zero_id=list(dt_zero_list[0])#convert dt_zero_list to list formate

    zero=[]
    for zero_id in dt_zero_id:
        zero.append(dt[zero_id])#just get 0.0
    dt=[val for val in dt if val not in zero]#if dt==0.0,del
    dtime=[]
    for i in range(0,len(jd)):
        jd_date=num2date(jd[i])
        jd_year_date=jd_date.replace(tzinfo=None)
        jd_year= jd_year_date.replace(year=int(yeartime))
        dtime.append(jd_year)
  
    return dtime,lat,lon



# save the output file, the format is ID, ESN, MONTH, day, HR(GMT), MIN, YEARDAY, lon, lat ,depth, temp
def save_output_file(path_output_file_name, id, time0, lat, lon, yeardays):
    fido=open(path_output_file_name,"w")
    fido.write("% id" + " "+"ESN"+" "+"MTH"+" "+"DAY"+" "+"HR(GMT)"+" "+"MIN"+" "+"YRDAY0"+" "+"LON"+" "+"LAT"+" "+"DEPTH"+" "+ "TEMP")
    for i in len(time0):
        fido.write(str(id).rjust(10)+ " " + "NaN"+" "+str(num2date(time0[i]).month).rjust(4)+ " " +
                   str(num2date(time0[i]).day).rjust(4)+ " "+str(num2date(time0[i]).hour).rjust(4)+ " "+
                   str(num2date(time0[i]).minute).rjust(4)+ " ")
        fido.write(("%10.6f") %(yeardays[i]))
        fido.write(" ")
        fido.write(("%10.6f") %(lon[i]))
        fido.write(" ")
        fido.write(("%10.6f") %(lat[i]))
        fido.write(" ")
        fido.write(("%5.1f") %(depth[i]))
        fido.write('NaN')
        fido.write('\n')
    fido.close()
    
#calculate the speed, when speed changed, plot the line use different colors
def calculate_speedcolors(lat,lon,id,yearday):
    #calculate the speed 
    speed=ll2uv(yearday,lat,lon)[2]
    #sort the speed and get the change index
    index=range(len(speed))
    index.sort(lambda x,y:cmp(speed[x],speed[y]))
    # get colors
    num_colors = len(speed)
    cmap = mpl.cm.jet
    cmap_value = scipy.linspace(0,1,num_colors)
    colors,speed_color = [],[]
    for i in cmap_value:
        colors.append(mpl.colors.colorConverter.to_rgb(cmap(i)))
    for i in index:
        speed_color.append(colors[i])
    return speed,speed_color
  
  
def plot_speedcolors(id,speed,time0,speed_color,lat,lon):
    # get the index when datetime.day change
    index_day=[]
    for i in range(1,len(time0)):
      if time0[i]<>time0[i-1]:
          index_day.append(i-1)
    # change time format to get the month and day
    month_time,day_time=[],[]
    for i in time0:
        month_time.append(dt.datetime.strptime(i,'%Y-%m-%d').month)
        day_time.append(dt.datetime.strptime(i,'%Y-%m-%d').day)  
    fig = plt.figure()
    plt.title('Difter#'+id)
    ax = fig.add_subplot(111)
    plt.xlabel('Longitude W')
    plt.ylabel('Latitude N')

    for i in range(1,len(speed)):
        plt.plot(lon[i-1:i+1],lat[i-1:i+1], '-',color=speed_color[i])
    # add text in the figure
    for i in index_day:
        ax.annotate(str(month_time[i])+"/"+str(day_time[i]), xy=(lon[i], lat[i]),  xycoords='data',
                  xytext=(10, 15), textcoords='offset points',
                  arrowprops=dict(arrowstyle="->"))
    #set the image position to get more place to plot color bar
    ax.set_position([0.125, .165, 0.8, .79])
    #add axes for color bar,the values are location of one more axes
    ax2 = fig.add_axes([0.125, 0.04, 0.8, 0.05])
    #set colorbar's range
    rawlins_norm = mpl.colors.Normalize(vmin=min(speed), vmax=max(speed))

    #plot color bar
    cb2 = mpl.colorbar.ColorbarBase(ax2, norm=rawlins_norm,orientation='horizontal')
    #a=np.linspace(int(min(speed)),int(max(speed)),4)
    #cb2.ax.set_xticks(np.linspace(min(speed),max(speed),))
    cb2.ax.set_xticklabels(['8cm/s', '16cm/s','24cm/s', '32cm/s', '40cm/s', '48cm/s', '56cm/s', '64cm/s'])
    plt.show()

