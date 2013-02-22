import csv
import datetime as dt
from matplotlib.dates import date2num


# TAPPY is a Tidal Analysis Program in Python
# u.txt and v.txt are from running tappy (After installing TAPPY, have input data and definition file then you can run tappy in doc. the input data and definition file have format)
# if you do not know how to use tappy, you can find the detail in oceanographic_python.doc/part 2/ chapter 2
#open u.txt and v.txt, read the time, u, v from the file and save the data to output file
def tappy_input_file(input_path,output_path,input_filename):
  output_filename_u="u.txt"
  output_filename_v="v.txt"
  dataReader = csv.reader(open(input_path+input_filename,'rb'))
  verts=[]
  for row in dataReader:
    verts.append(row)
  del verts[len(verts)-1],verts[0] #del the first line and last line
  sites,u,v,year,hour=[],[],[],[],[]
  for i in range(0,len(verts)):
    #convert "space delimite" to comma
    sites.append(verts[i][0].split()[0])
    year.append(verts[i][0].split()[1])
    hour.append(verts[i][0].split()[2])
    u.append(verts[i][0].split()[6])
    v.append(verts[i][0].split()[7])

  output_file=output_path+output_filename_u#"C:/xiuling/u.txt"
  f=open(output_file,"w")
  for site, i in zip(sites,xrange(len(sites))):
    f.write(site+" "+year[i][0:4]+year[i][5:7]+year[i][8:10]+" "+
            hour[i][0:2]+":"+hour[i][2:]+" "+hour[i][2:]+" "+str(u[i].rjust(5))+"\n")
  output_file=output_path+output_filename_v#"C:/xiuling/v.txt"
  f=open(output_file,"w")
  for site, i in zip(sites,xrange(len(sites))):
    f.write(site+" "+year[i][0:4]+year[i][5:7]+year[i][8:10]+" "+
            hour[i][0:2]+":"+hour[i][2:]+" "+hour[i][2:]+" "+str(v[i].rjust(5))+"\n")
  f.close

#after run tappy_input_file, we continue read the data from file
def tappy_read(filename):
    dataReader = csv.reader(open(filename,'rb'))
    verts=[]
    for row in dataReader:
        verts.append(row)
    date_time,tappy_data=[],[]
    for i in range(0,len(verts)):
        tappy_data.append(verts[i][0].split()[1])
        datetime=dt.datetime.strptime(verts[i][0].split()[0][0:10]+ " " +verts[i][0].split()[0][11:19],
                                      '%Y-%m-%d %H:%M:%S')
        date_time.append(date2num(datetime))
    tappy_data=[float(i) for i in tappy_data]
    return tappy_data,date_time
