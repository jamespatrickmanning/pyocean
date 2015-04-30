import sys
sys.path.append("../modules")
import basemap as bm
import matplotlib.pyplot as plt
import pylab
from pylab import ginput
import numpy as np

# extract coastline and bathymetry using pydap
plt.figure(1,figsize=(10,8))
#bm.basemap_detail([41.,43.5],[-72.,-69.0],True,True,0.5)
#bm.basemap_detail([41.0,43.5],[-72.,-69.0],True,False)
bm.basemap_standard([41.0,43.5],[-72.,-69.0], [2])
plt.title('PIs (white) and Partners (black)',fontsize=18)
plt.show()

sites=['GOMI','NESS','WHOI','SSC','SSNSC','WHSTEP','NEFSC','CCS','NGSS','CMHS','NEAq','SEA','SBNMS','WBWS','CSWA']
nums=len(sites)
print 'There are '+str(nums)+'sites'
'''pts=ginput(nums, timeout=120)
x=map(lambda x: x[0],pts) # map applies the function passed as 
y=map(lambda x: x[1],pts) # first parameter to each e
np.save('sites',[x,y])
'''
p=np.load('sites.npy')
x=p[0]
y=p[1]
for k in range(len(x)):
   plt.plot(x[k], y[k],'.',color='w')
   plt.annotate(sites[k],xy=(x[k],y[k]),xytext=(x[k]+.3,y[k]),arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()

PIs=['CCSCR','GOMLF','MEGSTTS','UMASSGHP']
nums=len(PIs)
print 'There are '+str(nums)+'PIs'
'''
pts=ginput(nums, timeout=120)
x=map(lambda x: x[0],pts) # map applies the function passed as 
y=map(lambda x: x[1],pts) # first parameter to each e
np.save('PIs',[x,y])
'''
p=np.load('PIs.npy')
x=p[0]
y=p[1]
for k in range(len(x)):
   plt.plot(x[k], y[k],'.',color='w')
   plt.annotate(PIs[k],xy=(x[k],y[k]),xytext=(x[k]-.8,y[k]),color='w',arrowprops=dict(facecolor='white', shrink=0.05))
plt.show()
plt.savefig('/net/nwebserver/drifter/MD_sitemap_2015.png')




