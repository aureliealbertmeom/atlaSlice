#!/usr/bin/env python
"""
This script takes as inputs :
  - a hourly 3D field defined in a region (ex: 3D temperature in aLS)
  - 3D velocity fields for the 3 directions (x, y, and z) at the same time and region
  - the coordinates of 1°x1° boxes for this particular region defined in params/boxes
and with it computes the daily mean profile for each boxes of:
    - the fluxes of the input quantity over the 3 dimensions
    - the fluxes of the 3dimensions gradients of the input quantity over the 3 dimensions
and finally it writes the outputs in one netcdf file per box and date
"""
import sys, getopt, os, glob, time
import argparse
import pandas as pd
import xarray as xr
import numpy as np
import datetime

from functions import data as da
from functions import functions as f
from functions import calc as ca
from params import simulations_dict as params
from params import slice_dict as sliced

machine = 'cal1'
config = 'eNATL60'
simu = 'BLBT02'
var = 'buoyancy'
reg = 'aGS'
freq = '1h'
date = '20090701'

def read_csv(machine,reg,config):
    boxes=pd.read_csv(sliced.params_path[machine]+'/boxes/boxes_'+str(reg)+'_1x1_'+str(config)+'.csv',sep = '\t',index_col=0)
    ibox=params.xy[config][reg][0]
    jbox=params.xy[config][reg][2]
    imin=boxes['imin']-ibox
    imax=boxes['imax']-ibox
    jmin=boxes['jmin']-jbox
    jmax=boxes['jmax']-jbox
    box_name=boxes.index
    return imin,imax,jmin,jmax,box_name

def mean_10_10_xyt(data):
    return data[:,:,10:-10,10:-10].mean(dim={'x','y','time_counter'})

def compute_buoy(t,s):
    rau0  = 1000
    grav  = 9.81
    buoy= -1*(grav/rau0)*sigma0(t,s)
    return buoy

def sigma0(t,s):
    zrau0=1000
    zsr=np.sqrt(np.abs(s))
    zs=s
    zt=t
    zr1 = ( ( ( ( 6.536332e-9*zt-1.120083e-6 )*zt+1.001685e-4)*zt - 9.095290e-3 )*zt+6.793952e-2 )*zt+999.842594
    zr2= ( ( ( 5.3875e-9*zt-8.2467e-7 )*zt+7.6438e-5 ) *zt - 4.0899e-3 ) *zt+0.824493
    zr3= ( -1.6546e-6*zt+1.0227e-4 ) *zt-5.72466e-3
    zr4= 4.8314e-4
    sigma0=( zr4*zs + zr3*zsr + zr2 ) *zs + zr1 - zrau0
    return sigma0

def compute_filt_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name):

    #Get the velocity data
    fileu=dirf+'/'+str(config)+str(reg)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_'+str(vel)+'.nc'
    data_box_vel=da.get_data3D_box(fileu,params.vars_name[config][simu][vel],imin,imax,jmin,jmax,k)

    #Interpolate at T points
    match vel:
        case 'U':
            data_box_velt=data_box_vel.interp(depthu=data_box.deptht)
        case 'V':
            data_box_velt=data_box_vel.interp(depthv=data_box.deptht)
        case 'W':
            data_box_velt=data_box_vel.interp(depthw=data_box.deptht)
    #Flux 
    flux_box=data_box*data_box_velt

    #Filt
    filt_data=ca.filt(flux_box)
    return filt_data

def compute_prof_filt_flux_gradients_onebox(data_box,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name):

    #Get the flux
    filt_data=compute_filt_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)
    
    #Get grid sizes
    fileh=params.mesh_hgr[machine][config][reg]
    e1=da.get_data2D_box(fileh,params.e1name[vel],imin,imax,jmin,jmax,k)
    e2=da.get_data2D_box(fileh,params.e2name[vel],imin,imax,jmin,jmax,k)
    filez=params.mesh_zgr[machine][config][reg]
    e3=da.get_data3D_box(filez,params.e3name[vel],imin,imax,jmin,jmax,k)
    e3t=e3.rename({'z':'deptht'})

    #Gradients
    data_dx=ca.dx_var(filt_data,e1)
    data_dy=ca.dy_var(filt_data,e2)
    data_dz=ca.dz_var(filt_data,e3t,params.depname[var])

    #Mean
    profile_data_dx=mean_10_10_xyt(data_dx.squeeze())
    profile_data_dy=mean_10_10_xyt(data_dy.squeeze())
    profile_data_dz=mean_10_10_xyt(data_dz.squeeze())
    return profile_data_dx,profile_data_dy,profile_data_dz


def compute_prof_filt_flux_onebox(data_box,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name):

    #Get the filtered flux
    filt_data=compute_filt_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)

    #Mean
    profile_data=mean_10_10_xyt(filt_data)
    return profile_data

def make_dataset_prof_flux_onebox(profile_data,attrs,var,vel,extras,extrab):

    match vel:
        case 'U':
            dirvel='x'
        case 'V':
            dirvel='y'
        case 'W':
            dirvel='z'
    dataset=profile_data.to_dataset(name=str(extras)+str(var)+'_flux_'+str(dirvel))
    if var == 'buoyancy':
        dataset[str(extras)+str(var)+'_flux_'+str(dirvel)].attrs['long_name']=str(extrab)+' Buoyancy_flux_'+str(dirvel)
        dataset[str(extras)+str(var)+'_flux_'+str(dirvel)].attrs['units']='m2/s3'
    else:
        dataset[str(extras)+str(var)+'_flux_'+str(dirvel)].attrs=attrs
        dataset[str(extras)+str(var)+'_flux_'+str(dirvel)].attrs['long_name']=str(extrab)+attrs['long_name']+'_flux_'+str(dirvel)
        dataset[str(extras)+str(var)+'_flux_'+str(dirvel)].attrs['units']=attrs['units']

    return dataset

def write_prof_filt_flux_gradients_onebox(machine,var,config,simu,reg,freq,date,imin,imax,jmin,jmax,box_name,k):
    # Path where the output are written
    dirf=sliced.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(simu)+'/'+str(freq)+'/'+str(reg)
    dirprof=dirf+'/profiles'

    # Create profiles sub-repo if not already existing
    if not os.path.exists(dirprof):
        os.makedirs(dirprof)

    # Name of the output file for one box and one date
    profile_name=dirprof+'/'+str(config)+str(reg)+box_name[k]+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_'+str(var)+'_fluxes_and_gradient_fluxes_profiles.nc'

    # Proceed only if the file does not exist yet
    if not os.path.exists(profile_name):
        list_dataset=[]

        #Get the input data
        if var == 'buoyancy':
            fileti=dirf+'/'+str(config)+str(reg)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_T.nc'
            filesi=dirf+'/'+str(config)+str(reg)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_S.nc'
            dataT=da.get_data3D_box(fileti,params.vars_name[config][simu]['T'],imin,imax,jmin,jmax,k)
            dataS=da.get_data3D_box(filesi,params.vars_name[config][simu]['S'],imin,imax,jmin,jmax,k)
            data_box=compute_buoy(dataT,dataS)
            attrs=dataT.attrs

        else:
            filei=dirf+'/'+str(config)+str(reg)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_'+str(var)+'.nc'
            data_box=da.get_data3D_box(filei,params.vars_name[config][simu][var],imin,imax,jmin,jmax,k)
            attrs=data_box.attrs

        #Make datasets with the profiles to be written : first the filtered fluxes
        for vel in [ 'U', 'V', 'W' ]:
            profile=compute_prof_filt_flux_onebox(data_box,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)
            dataset=make_dataset_prof_flux_onebox(profile,attrs,var,vel,'','')
            list_dataset.append(dataset)
    
            #Then the filtered gradients fluxes
            profile_data_dxu,dataset_data_dyu,dataset_data_dzu=compute_prof_filt_flux_gradients_onebox(data_box,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)
            dataset=make_dataset_prof_flux_onebox(profile_data_dxu,attrs,var,vel,'dx','dx gradient of ')
            list_dataset.append(dataset)
            dataset=make_dataset_prof_flux_onebox(profile_data_dxu,attrs,var,vel,'dy','dy gradient of ')
            list_dataset.append(dataset)
            dataset=make_dataset_prof_flux_onebox(profile_data_dxu,attrs,var,vel,'dz','dz gradient of ')
            list_dataset.append(dataset)
        
        # Mergining all the datasets
        big_dataset=xr.merge(list_dataset)
        big_dataset.attrs['global_attribute']= 'predictors profiles averaged over 24h and in '+box_name[k]+' computed on adastra CINES '+str(datetime.date.today())
        print('writing profile '+profile_name)
        big_dataset.to_netcdf(path=profile_name,mode='w')


print ('Averaging profiles of filtered fluxes of '+str(var)+' for simulation '+str(config)+'-'+str(simu)+' in 1°x1° boxes located in region '+str(reg))

imin,imax,jmin,jmax,box_name=read_csv(machine,reg,config)
write_prof_filt_flux_gradients_onebox(machine,var,config,simu,reg,freq,date,imin,imax,jmin,jmax,box_name,0)



