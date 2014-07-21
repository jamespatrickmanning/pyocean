# -*- coding: utf-8 -*-
import numpy as np

def get_fvcom_gom3_grid(a='disk'):
    """
    Grid=get_fvcom_gom3_grid(a='disk')
    
    returns FVCOM GOM3 triangular grid parameters
    
    input:
    a='disk' - quick load from disk, default 
    a='web' - get from web
    
    output:
    Grid={'x':x,'y':y,'xc':xc,'yc':yc,'lon':lon,'lat':lat,'lonc':lonc,'latc':latc,'coslat':coslat,'coslatc':coslatc,'kvf':kvf,'kff':kff,'kvv':kvv,'nvv':nvv,'kfv':kfv,'nfv':nfv}
    a dictionary with arrays difining FVCOM GOM3 triangular grid
    
    @author: Vitalii Sheremet, FATE Project, vsheremet@whoi.edu
    """
    
    if a=='disk':
    # quick load from disk
        print 'loading FVCOM GOM3 Grid parameters from disk'

        x=np.load('gom3.x.npy')
        y=np.load('gom3.y.npy')
        xc=np.load('gom3.xc.npy')
        yc=np.load('gom3.yc.npy')
        
        lon=np.load('gom3.lon.npy')
        lat=np.load('gom3.lat.npy')
        lonc=np.load('gom3.lonc.npy')
        latc=np.load('gom3.latc.npy')
        
        coslat=np.load('gom3.coslat.npy')
        coslatc=np.load('gom3.coslatc.npy')
        
        kvf=np.load('gom3.kvf.npy')
        kff=np.load('gom3.kff.npy')
        kvv=np.load('gom3.kvv.npy')
        nvv=np.load('gom3.nvv.npy')
        kfv=np.load('gom3.kfv.npy')
        nfv=np.load('gom3.nfv.npy')
    
        Grid={'x':x,'y':y,'xc':xc,'yc':yc,'lon':lon,'lat':lat,'lonc':lonc,'latc':latc,'coslat':coslat,'coslatc':coslatc,'kvf':kvf,'kff':kff,'kvv':kvv,'nvv':nvv,'kfv':kfv,'nfv':nfv}
    
    elif a=='web':
        
        #from pydap.client import open_url # pydap version
        from netCDF4 import Dataset        # netCDF4 version
        URL='http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3'
        #http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?
        #a1u[0:1:3][0:1:90414],a2u[0:1:3][0:1:90414],art1[0:1:48450],art2[0:1:48450],
        #aw0[0:1:2][0:1:90414],awx[0:1:2][0:1:90414],awy[0:1:2][0:1:90414],cc_hvc[0:1:90414],
        #h[0:1:48450],lat[0:1:48450],latc[0:1:90414],lon[0:1:48450],lonc[0:1:90414],
        #nbe[0:1:2][0:1:90414],nbsn[0:1:10][0:1:48450],nbve[0:1:8][0:1:48450],
        #nn_hvc[0:1:48450],nprocs,ntsn[0:1:48450],ntve[0:1:48450],nv[0:1:2][0:1:90414],
        #partition[0:1:90414],siglay[0:1:44][0:1:48450],siglev[0:1:45][0:1:48450],
        #x[0:1:48450],xc[0:1:90414],y[0:1:48450],yc[0:1:90414],z0b[0:1:90414],
        #Itime[0:1:171882],Itime2[0:1:171882],Times[0:1:171882],file_date[0:1:171882],
        #iint[0:1:171882],kh[0:1:171882][0:1:45][0:1:48450],
        #km[0:1:171882][0:1:45][0:1:48450],kq[0:1:171882][0:1:45][0:1:48450],
        #l[0:1:171882][0:1:45][0:1:48450],net_heat_flux[0:1:171882][0:1:48450],
        #omega[0:1:171882][0:1:45][0:1:48450],q2[0:1:171882][0:1:45][0:1:48450],
        #q2l[0:1:171882][0:1:45][0:1:48450],salinity[0:1:171882][0:1:44][0:1:48450],
        #short_wave[0:1:171882][0:1:48450],temp[0:1:171882][0:1:44][0:1:48450],
        #time[0:1:171882],u[0:1:171882][0:1:44][0:1:90414],ua[0:1:171882][0:1:90414],
        #uwind_stress[0:1:171882][0:1:90414],v[0:1:171882][0:1:44][0:1:90414],
        #va[0:1:171882][0:1:90414],vwind_stress[0:1:171882][0:1:90414],
        #ww[0:1:171882][0:1:44][0:1:90414],zeta[0:1:171882][0:1:48450]
        
        print 'getting FVCOM GOM3 Grid parameters from web'
        print URL
        
        #ds=open_url(URL)                 # pydap version 
        ds = Dataset(URL,'r').variables   # netCDF4 version
        
        #xxx=ds['xxx']; np.save('gom3.xxx.npy',np.array(xxx))
        print 'getting a1u a2u'
        a1u=ds['a1u']; np.save('gom3.a1u.npy',np.array(a1u))
        a2u=ds['a2u']; np.save('gom3.a2u.npy',np.array(a2u))
        print 'getting art1 art2'
        art1=ds['art1']; np.save('gom3.art1.npy',np.array(art1))
        art2=ds['art2']; np.save('gom3.art2.npy',np.array(art2))
        print 'getting aw0 awx awy'
        aw0=ds['aw0']; np.save('gom3.aw0.npy',np.array(aw0))
        awx=ds['awx']; np.save('gom3.awx.npy',np.array(awx))
        awy=ds['awy']; np.save('gom3.awy.npy',np.array(awy))
        print 'getting cc_hvc'
        cc_hvc=ds['cc_hvc']; np.save('gom3.cc_hvc.npy',np.array(cc_hvc))
            
        print 'getting bathymetry'    
        h=ds['h']; np.save('gom3.h.npy',np.array(h))
        
        print 'getting lon,lat'
        lat=ds['lat']; np.save('gom3.lat.npy',np.array(lat))
        lon=ds['lon']; np.save('gom3.lon.npy',np.array(lon))
        latc=ds['latc']; np.save('gom3.latc.npy',np.array(latc))
        lonc=ds['lonc']; np.save('gom3.lonc.npy',np.array(lonc))
        
        print 'getting connectivity info'
        nbe=ds['nbe']; np.save('gom3.nbe.npy',np.array(nbe))
        nbsn=ds['nbsn']; np.save('gom3.nbsn.npy',np.array(nbsn))
        nbve=ds['nbve']; np.save('gom3.nbve.npy',np.array(nbve))
        nn_hvc=ds['nn_hvc']; np.save('gom3.nn_hvc.npy',np.array(nn_hvc))
        nprocs=ds['nprocs']; np.save('gom3.nprocs.npy',np.array(nprocs))
        ntsn=ds['ntsn']; np.save('gom3.ntsn.npy',np.array(ntsn))
        ntve=ds['ntve']; np.save('gom3.ntve.npy',np.array(ntve))
        nv=ds['nv']; np.save('gom3.nv.npy',np.array(nv))
        partition=ds['partition']; np.save('gom3.partition.npy',np.array(partition))
        
        print 'getting siglay, siglev'
        siglay=ds['siglay']; np.save('gom3.siglay.npy',np.array(siglay))
        siglev=ds['siglev']; np.save('gom3.siglev.npy',np.array(siglev))
        
        print 'getting Cartesian coord'
        x=ds['x']; np.save('gom3.x.npy',np.array(x))
        xc=ds['xc']; np.save('gom3.xc.npy',np.array(xc))
        y=ds['y']; np.save('gom3.y.npy',np.array(y))
        yc=ds['yc']; np.save('gom3.yc.npy',np.array(yc))
            
        """    
        x=np.load('gom3.x.npy')
        y=np.load('gom3.y.npy')
        xc=np.load('gom3.xc.npy')
        yc=np.load('gom3.yc.npy')
        
        lon=np.load('gom3.lon.npy')
        lat=np.load('gom3.lat.npy')
        lonc=np.load('gom3.lonc.npy')
        latc=np.load('gom3.latc.npy')
        """
        # precalculate Lame coefficients for the spherical coordinates
        coslat=np.cos(lat*np.pi/180.)
        coslatc=np.cos(latc*np.pi/180.)
        
        print 'renaming variables'
        # In the following: kvf,kff,kvv,nvv,kfv,nfv 
        # k indicates index (zero based), 
        # n indicates the number of items
        
        #nv: Array of 32 bit Integers [three = 0..2][nele = 0..90414] 
        #long_name: nodes surrounding element
        #standard_name: face_node_connectivity
        #start_index: 1
        nv=np.load('gom3.nv.npy')
        # vertices corresponding to a given face
        kvf=nv-1 # convert from FORTRAN to python 0-based indexing
        #nv-=1 # convert from FORTRAN to python 0-based indexing
        #kvf=nv
        
        #nbe: Array of 32 bit Integers [three = 0..2][nele = 0..90414] 
        # long_name: elements surrounding each element
        nbe=np.load('gom3.nbe.npy')
        # faces surrounding a given face
        kff=nbe-1 # convert from FORTRAN to python 0-based indexing
        #nbe-=1 # convert from FORTRAN to python 0-based indexing
        #kff=nbe
        
        #nbsn: Array of 32 bit Integers [maxnode = 0..10][node = 0..48450]
        #long_name: nodes surrounding each node
         # list of nodes surrounding a given node, 1st and last entries identical to make a closed loop
        nbsn=np.load('gom3.nbsn.npy')
        # vertices surrounding a given vertex
        kvv=nbsn-1 # convert from FORTRAN to python 0-based indexing
        #nbsn-=1 # convert from FORTRAN to python 0-based indexing
        #kvv=nbsn
        
        #ntsn: Array of 32 bit Integers [node = 0..48450]
        #long_name: #nodes surrounding each node
         # the number of nodes surrounding a given node + 1, because 1st and last entries identical to make a closed loop
        ntsn=np.load('gom3.ntsn.npy')
        # number of vertices surrounding a given vertex
        nvv=ntsn
        
        #nvv=ntsn
        
        #nbve: Array of 32 bit Integers [maxelem = 0..8][node = 0..48450] 
        #long_name: elems surrounding each node
        # list of elements surrounding a given node, 1st and last entries identical to make a closed loop
        nbve=np.load('gom3.nbve.npy')
        # faces surrounding a given vertex
        kfv=nbve-1 # convert from FORTRAN to python 0-based indexing
        #nbve-=1 # convert from FORTRAN to python 0-based indexing
        #kfv=nbve
        
        #ntve: Array of 32 bit Integers [node = 0..48450] 
        #long_name: #elems surrounding each node
        # the number of elements surrounding a given node + 1, because 1st and last entries identical to make a closed loop
        ntve=np.load('gom3.ntve.npy')
        # number of faces surrounding a given vertex
        nfv=ntve
        #nfv=ntve
        
        #Grid={'x':x,'y':y,'xc':xc,'yc':yc,'lon':lon,'lat':lat,'lonc':lonc,'latc':latc,'coslat':coslat,'coslatc':coslatc,'kvf':nv,'kff':nbe,'kvv':nbsn,'nvv':ntsn,'kfv':nbve,'nfv':ntve}
        Grid={'x':x,'y':y,'xc':xc,'yc':yc,'lon':lon,'lat':lat,'lonc':lonc,'latc':latc,'coslat':coslat,'coslatc':coslatc,'kvf':kvf,'kff':kff,'kvv':kvv,'nvv':nvv,'kfv':kfv,'nfv':nfv}
        
        np.save('gom3.coslat.npy',coslat)
        np.save('gom3.coslatc.npy',coslatc)
        np.save('gom3.kvf.npy',kvf)
        np.save('gom3.kff.npy',kff)
        np.save('gom3.kvv.npy',kvv)
        np.save('gom3.nvv.npy',nvv)
        np.save('gom3.kfv.npy',kfv)
        np.save('gom3.nfv.npy',nfv)

    
    else:
        print 'get_fvcom_gom3_grid: unknown argument'

    return Grid
    
if __name__ == "__main__":
    try:
        Grid=get_fvcom_gom3_grid('disk')
    except:
        Grid=get_fvcom_gom3_grid('web')
    
