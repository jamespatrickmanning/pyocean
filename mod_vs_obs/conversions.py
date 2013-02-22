import numpy as np
import math
from matplotlib.dates import num2date


# convert celsius degree to fahrenheit degree
def c2f(*c):
  "convert Celsius to Fahrenheit"
  if len(c)<1:
    c=input ('what Celsius?')
    f=1.8*c+32
    return f
  else:
    for k in range(1,len(c)+1):
      f=c[k-1]*1.8 + 32
      return f

def cmps2knots(cmps):
  kmperhr=float(cmps)/100000*3600
  knots=kmperhr/1.8535
  return knots


# convert number of datetime to yearday
def date2yd(datetime_nums):
  "convert date to yearday"
  # imput must be a list of numbers  
  yearday=[]
  for datetime_num in datetime_nums:
    year_day=num2date(datetime_num).strftime('%j')
    year_time=float(num2date(datetime_num).hour+(float(num2date(datetime_num).minute)/float(60))+(float(num2date(datetime_num).second)/float(3600)))/float(24)
    yearday.append(float(year_day)+year_time)
  return yearday

#convert decimal value to degrees,minutes
def dd2dm(lat,lon):
  lat,lon=np.asarray(lat),np.asarray(lon)
  lat_dd=abs(lat)
  lat_d=math.floor(lat_dd)
  lat_m=(lat_dd-lat_d)*60

  lon_dd=abs(lon)
  lon_d=math.floor(lon_dd)
  lon_m=(lon_dd-lon_d)*60
  #return u'%d\N{DEGREE SIGN}%g' %(lat_d,lat_m),u'%d\N{DEGREE SIGN}%g' %(lon_d,lon_m)  
  la=lat_dd*100+lat_m
  lo=lon_dd*100+lon_m
  return la,lo
  #str(int(lat_d)\N{DEGREE SIGN})+str(lat_m)#,lat_s, lon_d,lon_m,lon_s)
  #(u"%d\N{DEGREE SIGN} %g' %s")

#convert decimal value to degrees,minutes,seconds
def dd2dms(lat,lon):
  lat,lon=np.asarray(lat),np.asarray(lon)
  lat_dd=abs(lat)
  lat_d=math.floor(lat_dd)
  lat_m=math.floor((lat_dd-lat_d)*60)
  lat_s=((lat_dd-lat_d)*60-lat_m)*60
  if lon<0:
    lon_dd=abs(lon)
    lon_d=math.floor(lon_dd)
    lon_m=math.floor((lon_dd-lon_d)*60)
    lon_s=((lon_dd-lon_d)*60-lon_m)*60
    lon_d=-lon_d
  else:
    lon_dd=abs(lon)
    lon_d=math.floor(lon_dd)
    lon_m=math.floor((lon_dd-lon_d)*60)
    lon_s=((lon_dd-lon_d)*60-lon_m)*60
  return int(lat_d),int(lat_m),float(lat_s), int(lon_d),int(lon_m),float(lon_s)

def dens0(s, t):
  b0 =  8.24493e-1
  b1 = -4.0899e-3
  b2 =  7.6438e-5
  b3 = -8.2467e-7
  b4 =  5.3875e-9

  c0 = -5.72466e-3
  c1 =  1.0227e-4
  c2 = -1.6546e-6

  d0 = 4.8314e-4
  T68  = T68conv(t)
  dens0 = smow(t) + ( b0 + ( b1 + ( b2 + ( b3 + b4 * T68 ) * T68 ) * T68 ) * T68 ) * \
  s + ( c0 + ( c1 + c2 * T68 ) * T68 ) * s * (s)**0.5 + d0 * s**2
  return dens0

def dens(s, t, p):
  s, t, p = np.asarray(s), np.asarray(t), np.asarray(p)
  densP0 = dens0(s, t)
  K = seck(s, t, p)
  p = p / 10.0 # convert from db to atm pressure units
  dens = densP0 / ( 1-p / K )
  return dens
  
def depth(p, lat):
  p, lat = np.asarray(p), np.asarray(lat)
    # Eqn 25, p26.  UNESCO 1983.
  c1 =  9.72659
  c2 = -2.2512E-5
  c3 =  2.279E-10
  c4 = -1.82E-15

  gam_dash = 2.184E-6

  lat = abs(lat)
  X   = np.sin( np.deg2rad(lat) )
  X   = X * X

  bot_line = 9.780318 * ( 1.0 + ( 5.2788E-3 + 2.36E-5 * X ) * X ) + \
               gam_dash * 0.5 * p
  top_line = ( ( ( c4 * p + c3 ) * p + c2 ) * p + c1 ) * p
  depth = top_line / bot_line
  return depth

# calculate the distanse between two points(latitude,longitude)
def dist(lat1, lon1, lat2, lon2):
  "compute distance between two points,you need to input coordinate(lat,lon) of both points"
  if 1000>(lon1)>0:
    (lat1,lon1)=dd2dm(lat1,lon1)
  if 1000>(lon2)>0: 
    (lat2,lon2)=dd2dm(lat2,lon2)
  pid180=math.pi/180
  alat=(lat1)*pid180
  alon=(lon1)*pid180
  blat=(lat2)*pid180
  blon=(lon2)*pid180
  
  cix=math.cos(alat)*math.cos(alat)*math.cos(alon-blon)+math.sin(alat)*math.sin(alat)
  distkmx=6371*math.tan(math.sqrt(abs(1-cix*cix)/cix))
  ciy=math.cos(alat)*math.cos(blat)*math.cos(alon-alon)+math.sin(alat)*math.sin(blat) 
  distkmy=6371*math.tan(math.sqrt(abs(1-ciy*ciy)/ciy))

  if distkmx>0.001:   
    bear=abs(math.atan(distkmy/distkmx))
    if blon>alon and blat>alat:
        bear=90-bear*180/math.pi 
    elif blon>alon and blat<=alat:
        bear=90+bear*180/math.pi
    elif blon<alon and blat<=alat:        
        bear=270-bear*180/math.pi
    elif blon<alon and blat>alat:  
        bear=270+bear*180/math.pi
  
  else:
    if blat>=alat:
        bear=0
    else:
        bear=180

  ci=math.cos(alat)*math.cos(blat)*math.cos(alon-blon)+math.sin(alat)*math.sin(blat)
  distkm=6371*math.tan(math.sqrt(abs(1-ci*ci)/ci))
  return distkm,bear

#convert degrees, minutes to decimal
def dm2dd(lat,lon):
    (a,b)=divmod(float(lat),100)   
    aa=int(a)
    bb=float(b)
    lat_value=aa+bb/60

    if float(lon)<0:
        (c,d)=divmod(abs(float(lon)),100)
        cc=int(c)
        dd=float(d)
        lon_value=cc+(dd/60)
        lon_value=-lon_value
    else:
        (c,d)=divmod(float(lon),100)
        cc=int(c)
        dd=float(d)
        lon_value=cc+(dd/60)
    return lat_value, -lon_value


def f2c(*f):
  "convert Fahrenheit to Celsius "
  if len(f)<1:
    f=input('what Fahrenheit?')
    c=(f-32)/1.8
    return c
  else:
    for k in range(1,len(f)+1):
      c=(f[k-1]-32)/1.8
      return c

def fth2m(fth):
  m=fth*1.8288
  return m

def knots2ms(knots):
  kmperhour=knots*1.8535
  meterspersecond=kmperhour*1000./3600.
  return meterspersecond

#change lat,lon to u, v
def ll2uv(jd,lat,lon):#jd is yearday
  "baced on yearday,lat,lon.  you can get latitude speed and longitude speed "
  time=list(np.diff(jd))
  diff_time_list=[]
  for i in time:
      diff_time_list.append(float(i)*24*60*60)
 
  u,v,jdn,spd=[],[],[],[]
  for i in range(1,len(jd)):
    (dkm,bear)=dist(lat[i-1],lon[i-1],lat[i],lon[i])
    u.append(sd2uv(float(dkm*100000)/diff_time_list[i-1],bear)[0])
    v.append(sd2uv(float(dkm*100000)/diff_time_list[i-1],bear)[1])
    spd.append(np.sqrt(u[i-1]**2+v[i-1]**2))
    jdn.append(float(diff_time_list[i-1])/2/24/60/60+jd[i-1])
  return u,v,spd,jdn

def m2fth(m):
  fth=m/1.8288
  return fth


def sd2uv(s,d):
    u=float(s)*math.sin(math.pi*float(d)/180.)
    v=float(s)*math.cos(math.pi*float(d)/180.)
    return u,v



def smow(t):
  t = np.asarray(t)
  a0 = 999.842594
  a1 =   6.793952e-2
  a2 =  -9.095290e-3
  a3 =   1.001685e-4
  a4 =  -1.120083e-6
  a5 =   6.536332e-9
  
  T68  = T68conv(t)
  
  dens = a0 + ( a1 + ( a2 + ( a3 + ( a4 + a5 * T68 ) * T68 ) * T68 ) * T68 ) * T68
  return dens

def seck(s, t, p=0):
  s, t, p = np.asarray(s), np.asarray(t), np.asarray(p)

    # Compute compression terms
  p   = p/10.0 # convert from db to atmospheric pressure units
  T68 = T68conv(t)

    # Pure water terms of the secant bulk modulus at atmos pressure.
    # UNESCO eqn 19 p 18
  h3 = -5.77905E-7
  h2 =  1.16092E-4
  h1 =  1.43713E-3
  h0 =  3.239908   #[-0.1194975]

  AW = h0 + ( h1 + ( h2 + h3 * T68 ) * T68 ) * T68

  k2 =  5.2787E-8
  k1 = -6.12293E-6
  k0 =  8.50935E-5  #[+3.47718E-5]

  BW = k0 + ( k1 + k2 * T68 ) * T68

  e4 =    -5.155288E-5
  e3 =     1.360477E-2
  e2 =    -2.327105
  e1 =   148.4206
  e0 = 19652.21    #[-1930.06]

  KW  = e0 + ( e1 + ( e2 + ( e3 + e4 * T68 ) * T68 ) * T68 ) * T68 # eqn 19

    # Sea water terms of secant bulk modulus at atmos. pressure
  j0 = 1.91075E-4

  i2 = -1.6078E-6
  i1 = -1.0981E-5
  i0 =  2.2838E-3

  SR = (s)**0.5

  A  = AW + ( i0 + ( i1 + i2 * T68 ) * T68 + j0 * SR ) * s

  m2 =  9.1697E-10
  m1 =  2.0816E-8
  m0 = -9.9348E-7
  B = BW + ( m0 + ( m1 + m2 * T68 ) * T68 ) * s # eqn 18
  f3 =  -6.1670E-5
  f2 =   1.09987E-2
  f1 =  -0.603459
  f0 =  54.6746
  g2 = -5.3009E-4
  g1 =  1.6483E-2
  g0 =  7.944E-2
  K0 = KW + ( f0 + ( f1 + ( f2 + f3 * T68 ) * T68 ) * T68 \
            + ( g0 + ( g1 + g2 * T68 ) * T68 ) * SR ) * s # eqn 16
  K = K0 + ( A + B * p ) * p # eqn 15
  return K



def sigmat(s, t, p):
  s, t, p = np.asarray(s), np.asarray(t), np.asarray(p)
  sgmt = dens(s, t, p) - 1000.0
  return sgmt
  
def T68conv(T90):
  T90 = np.asarray(T90)
  T68 = T90 * 1.00024
  return T68

def uv2sd(u,v):
  if u<>0:
    d=math.atan(float(v/u))*180/math.pi
    if u>0 and v>0:
      d=90-d
    if u>0 and v<=0:
      d=90+abs(d)
    if u<0 and v>0:
      d=270+abs(d)
    if u<0 and v<=0:
      d=270-abs(d)
  if u==0:
    if v<0:d=180
    else: d=0
  s=math.sqrt(u**2+v**2)
  return s,d
