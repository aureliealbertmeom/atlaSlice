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

def read_csv(machine,reg,config):
    boxes=pd.read_csv(sliced.params_path[machine]+'/boxes/boxes_'+str(reg)+'_1x1_'+str(config)+'.csv',sep = '\t',index_col=0)
    ibox=params.xy[config][reg][0]
    jbox=params.xy[config][reg][2]
    imin=boxes['imin']-ibox[box]
    imax=boxes['imax']-ibox[box]
    jmin=boxes['jmin']-jbox[box]
    jmax=boxes['jmax']-jbox[box]
    box_name=boxes.index
    return imin,imax,jmin,jmax,box_name

def mean_10_10_xyt(data):
    return data[:,:,10:-10,10:-10].mean(dim={'x','y','time_counter'})

def compute_prof_filt_onebox(dirf,config,simu,var,date,k,imin,imax,jmin,jmax,reg,box_name):

    filei=dirf+'/'+str(config)+str(reg)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_'+str(var)+'.nc'
    data_box=da.get_data3D_box_from_reg(filei,params.vars_name[config][simu][var],imin,imax,jmin,jmax,k)
    filt_data=ca.filt(data_box)
    profile_data=mean_10_10_xyt(filt_data)
    
    return profile_data

def compute_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name):

    #Get the velocity data
    fileu=dirf+'/'+str(config)+str(box)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_'+str(vel)+'.nc'
    data_box_vel=da.get_data3D_box_from_reg(filei,params.vars_name[config][simu][vel],imin,imax,jmin,jmax,k)

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
    return flux_box

def compute_prof_flux_gradients_onebox(data_box,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name):

    #Get the flux
    flux_box=compute_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)
    
    #Get grid sizes
    fileh=params.mesh_hgr[machine][config][reg]
    e1=da.get_data3D_box_from_reg(fileh,params.e1name[vel],imin,imax,jmin,jmax,k)
    e2=da.get_data3D_box_from_reg(fileh,params.e2name[vel],imin,imax,jmin,jmax,k)
    filez=params.mesh_zgr[machine][config][reg]
    e3=da.get_data3D_box_from_reg(filez,params.e3name[vel],imin,imax,jmin,jmax,k)
    e3t=e3.rename({'z':'deptht'})

    #Gradients
    data_dx=ca.dx_var(flux_box,e1)
    data_dy=ca.dy_var(flux_box,e2)
    data_dz=ca.dz_var(flux_box,e3t,params.depname[vel])

    #Mean
    profile_data_dx=mean_10_10_xyt(data_dx)
    profile_data_dy=mean_10_10_xyt(data_dy)
    profile_data_dz=mean_10_10_xyt(data_dz)
    return profile_data_dx,profile_data_dy,profile_data_dz


def compute_prof_flux_onebox(data_box,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name):

    #Get the flux
    flux_box=compute_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)

    #Mean
    profile_data=mean_10_10_xyt(flux_box)
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
    dataset[str(var)+'_flux_'+str(dirvel)].attrs=attrs
    dataset[str(var)+'_flux_'+str(dirvel)].attrs['standard_name']=str(extrab)+attrs['standard_name']
    dataset[str(var)+'_flux_'+str(dirvel)].attrs['long_name']=str(extrab)+attrs['long_name']
    dataset[str(var)+'_flux_'+str(dirvel)].attrs['units']=attrs['units']

    return dataset

def write_prof_flux_gradients_onebox(machine,var,config,simu,reg,freq,date,imin,imax,jmin,jmax,box_name,k):
    # Path where the output are written
    dirf=sliced.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(sim)+'/'+str(freq)+'/'+str(reg)
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
        filei=dirf+'/'+str(config)+str(reg)+'-'+str(simu)+'_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'.'+str(freq)+'_'+str(var)+'.nc'
        data_box=da.get_data3D_box_from_reg(filei,params.vars_name[config][simu][var],imin,imax,jmin,jmax,k)
        attrs=data_box.attrs

        #Make datasets with the profiles to be written : first the fluxes
        for vel in [ 'U', 'V', 'W' ]:
            profile=compute_prof_flux_onebox(data_box,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)
            dataset=make_dataset_prof_flux_onebox(profile,attrs,var,vel,'','')
            list_dataset.append(dataset)
    
            #Then the gradients fluxes
            profile_data_dxu,dataset_data_dyu,dataset_data_dzu=compute_prof_flux_gradients_onebox(data_box,attrs,machine,dirf,config,simu,var,vel,date,k,imin,imax,jmin,jmax,reg,box_name)
            dataset=make_dataset_prof_flux_onebox(profile_data_dxu,attrs,var,vel,'dx','dx gradient of ')
            list_dataset.append(dataset)
            dataset=make_dataset_prof_flux_onebox(profile_data_dxu,attrs,var,vel,'dy','dy gradient of ')
            list_dataset.append(dataset)
            dataset=make_dataset_prof_flux_onebox(profile_data_dxu,attrs,var,vel,'dz','dz gradient of ')
            list_dataset.append(dataset)
        
        # Mergining all the datasets
        big_dataset=xr.merge(list_dataset)
        big_dataset.attrs['global_attribute']= 'predictors profiles averaged over 24h and in '+box_name[ibox]+' computed on adastra CINES '+str(today)
        print('writing to netcdf')
        big_dataset.to_netcdf(path=profile_name,mode='w')

def parse_args():
    parser=argparse.ArgumentParser(description="all the plots")
    parser.add_argument('-mach',type=str,help='machine on which the plot is launched')
    parser.add_argument('-config',type=str,help='name of configuration')
    parser.add_argument('-simu',type=str,help='name of simulation')
    parser.add_argument('-var',type=str,help='name of variable')
    parser.add_argument('-reg',type=str,default='global',help='name of region')
    parser.add_argument('-freq',type=str,help='frequency of variable')
    parser.add_argument('-date',type=str,help='date of file')
    args=parser.parse_args()
    return args

def main():
    machine = parse_args().mach
    config = parse_args().config
    sim = parse_args().simu
    var = parse_args().var
    reg = parse_args().reg
    freq = parse_args().freq
    date = parse_args().date

    print ('Averaging profiles of fluxes of '+str(var)+' and filtering it for simulation '+str(config)+'-'+str(sim)+' in 1°x1° boxes located in region'+str(reg))

    imin,imax,jmin,jmax,box_name=read_csv(machine,reg,config)
    for k in np.arange(sliced.nb_boxes[config][reg]+1):
        write_prof_flux_gradients_onebox(machine,var,config,simu,reg,freq,date,imin,imax,jmin,jmax,box_name,k)



if __name__ == "__main__":
    main()
