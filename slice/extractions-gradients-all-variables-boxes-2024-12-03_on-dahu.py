#!/usr/bin/env python
#
"""
This script extracts profiles of temperature, salinity and 3D velocities in 1°x1° boxes in eNATL60-BLBT02 and compute buoyancy and 3D gradients of all quantities. Then it average over the box and over 24h and save it to a single file
Update : boxes aGS, aLS and aMNA have been extracted first and all the products are now computed 
"""

##imports

import xarray as xr 
import dask 
import numpy as np 
import os 
import time 
import glob
import datetime
import pandas as pd
import sys

today=datetime.date.today()

## data location and gridfile

import sys
sys.path.insert(0,'/lus/work/NAT/gda2307/aalbert/DEV/git/xscale')
import xscale

data_dir = '/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-BLBT02-S/1h/'
data_dir1 = '/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-BLBT02X-S/1h/'
grid_dir='/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-I'

## box indices 
def read_csv(box):
    boxes=pd.read_csv('/lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice/boxes_'+str(box)+'_1x1_eNATL60.csv',sep = '\t',index_col=0)
    ibox={'GS':1602,'LS':2686,'MNA':3462}
    jbox={'GS':1736,'LS':3589,'MNA':2337}
    imin=boxes['imin']-ibox[box]
    imax=boxes['imax']-ibox[box]
    jmin=boxes['jmin']-jbox[box]
    jmax=boxes['jmax']-jbox[box]
    box_name=boxes.index
    return imin,imax,jmin,jmax,box_name

## functions useful for computations

def dx_var(data,e1):
    dx_var = (data.shift(x=-1) - data)/e1
    return dx_var
def dy_var(data,e2):
    dy_var = (data.shift(y=-1) - data)/e2
    return dy_var
def dz_var(data,e3,dimdep):
    if dimdep == 'deptht':
        dz_var = (data.shift(deptht=-1) - data)/e3
    if dimdep == 'depthu':
        dz_var = (data.shift(depthu=-1) - data)/e3
    if dimdep == 'depthv':
        dz_var = (data.shift(depthv=-1) - data)/e3
    if dimdep == 'depthw':
        dz_var = (data.shift(depthw=-1) - data)/e3
    return dz_var

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

def filt(w):
    win_box2D = w.window
    win_box2D.set(window='hann', cutoff=20, dim=['x', 'y'], n=[30, 30],chunks={})
    bw = win_box2D.boundary_weights(drop_dims=[])
    w_LS = win_box2D.convolve(weights=bw)
    w_SS=w-w_LS
    return w_SS


## correspondance of dimensions and grids for each variable
filetyps = {'buoyancy_flux_x' : 'U','buoyancy_flux_y' : 'V', 'buoyancy_flux_z' : 'W','buoyancy' : 'T','votemper' : 'T', 'vosaline' : 'S','vozocrtx' : 'U', 'vomecrty' : 'V','vovecrtz' : 'W','vozocrtxSS' : 'U', 'vomecrtySS' : 'V','vovecrtzSS' : 'W'}
filedeps = {'buoyancy_flux_x' : 'deptht', 'buoyancy_flux_y' : 'deptht', 'buoyancy_flux_z' : 'deptht','buoyancy' : 'deptht','votemper' : 'deptht','vosaline' : 'deptht','vozocrtx' : 'depthu', 'vomecrty' : 'depthv','vovecrtz':'depthw','vozocrtxSS' : 'depthu', 'vomecrtySS' : 'depthv','vovecrtzSS':'depthw'}
var_help = {'vozocrtxSS' : 'vozocrtx', 'vomecrtySS' : 'vomecrty','vovecrtzSS':'vovecrtz','buoyancy_flux_x' : 'vozocrtx', 'buoyancy_flux_y' : 'vomecrty', 'buoyancy_flux_z':'vovecrtz'}
filee1 = {'buoyancy_flux_x' : 'e1t', 'buoyancy_flux_y' : 'e1t', 'buoyancy_flux_z' : 'e1t','buoyancy' : 'e1t','votemper' : 'e1t','vosaline' : 'e1t','vozocrtx' : 'e1u', 'vomecrty' : 'e1v','vovecrtz':'e1f','vozocrtxSS' : 'e1u', 'vomecrtySS' : 'e1v','vovecrtzSS':'e1f'}
filee2 = {'buoyancy_flux_x' : 'e2t', 'buoyancy_flux_y' : 'e2t', 'buoyancy_flux_z' : 'e2t','buoyancy' : 'e2t','votemper' : 'e2t','vosaline' : 'e2t','vozocrtx' : 'e2u', 'vomecrty' : 'e2v','vovecrtz':'e2f','vozocrtxSS' : 'e2u', 'vomecrtySS' : 'e2v','vovecrtzSS':'e2f'}
filee3 = {'buoyancy_flux_x' : 'e3t_0', 'buoyancy_flux_y' : 'e3t_0', 'buoyancy_flux_z' : 'e3t_0','buoyancy' : 'e3t_0','votemper' : 'e3t_0','vosaline' : 'e3t_0','vozocrtx' : 'e3u_0', 'vomecrty' : 'e3v_0','vovecrtz':'e3w_0','vozocrtxSS' : 'e3u_0', 'vomecrtySS' : 'e3v_0','vovecrtzSS':'e3w_0'}

## main computation function

def compute_all_profiles(var,date,ibox,imin,imax,jmin,jmax,box,box_name):
    print('compute profile of '+var)
    if var == 'buoyancy' or var == 'buoyancy_flux_x' or var == 'buoyancy_flux_y' or var == 'buoyancy_flux_z':
        if (int(date[4:6]) == 11 and int(date[6:9]) > 6) or (int(date[4:6]) > 11) or (int(date[0:4]) == 2010):
           filenameT = sorted(glob.glob(data_dir1+'a'+str(box)+'/eNATL60a'+str(box)+'-BLBT02X_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_T.nc'))
        else:
           filenameT = sorted(glob.glob(data_dir+'a'+str(box)+'/eNATL60a'+str(box)+'-BLBT02_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_T.nc'))
        fileT=filenameT[0]
        dsT=xr.open_dataset(fileT,chunks={'time_counter':1,'x':1000,'y':1000})
        data_boxT=dsT['votemper'][:,:,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
        if (int(date[4:6]) == 11 and int(date[6:9]) > 6) or (int(date[4:6]) > 11) or (int(date[0:4]) == 2010):
           filenameS = sorted(glob.glob(data_dir1+'a'+str(box)+'/eNATL60a'+str(box)+'-BLBT02X_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_S.nc'))
        else:
           filenameS = sorted(glob.glob(data_dir+'a'+str(box)+'/eNATL60a'+str(box)+'-BLBT02_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_S.nc'))
        fileS=filenameS[0]
        dsS=xr.open_dataset(fileS,chunks={'time_counter':1,'x':1000,'y':1000})
        data_boxS=dsS['vosaline'][:,:,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
        data_box=compute_buoy(data_boxT,data_boxS)

        if var == 'buoyancy_flux_x' or var == 'buoyancy_flux_y' or var == 'buoyancy_flux_z':
            data_box_buoyancy=data_box
            if (int(date[4:6]) == 11 and int(date[6:9]) > 6) or (int(date[4:6]) > 11) or (int(date[0:4]) == 2010):
               filename = sorted(glob.glob(data_dir1+'a'+str(box)+'/eNATL60a'+str(box)+'-BLBT02X_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_'+str(filetyps[var])+'.nc'))
            else:
               filename = sorted(glob.glob(data_dir+'a'+str(box)+'/eNATL60a'+str(box)+'-BLBT02_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_'+str(filetyps[var])+'.nc'))
            file=filename[0]
            ds=xr.open_dataset(file,chunks={'time_counter':1,'x':1000,'y':1000})
            data_box_vel=ds[str(var_help[var])][:,:,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
            if filedeps[var_help[var]]=='depthw':
                data_box_velt=data_box_vel.interp(depthw=data_box_buoyancy.deptht)
            if filedeps[var_help[var]]=='depthu':
                data_box_velt=data_box_vel.interp(depthu=data_box_buoyancy.deptht)
            if filedeps[var_help[var]]=='depthv':
                data_box_velt=data_box_vel.interp(depthv=data_box_buoyancy.deptht)
            data_box = data_box_buoyancy*data_box_velt
            attrs=data_box.attrs
            filt_data=filt(data_box)
            print('filtering of '+var+' ok')
            if var == 'buoyancy_flux_x':
               attrs['standard_name']='Buoyancy_flux_x'
               attrs['long_name']='Zonal Buoyancy flux'
               attrs['units']='m2/s3'
            if var == 'buoyancy_flux_y':
               attrs['standard_name']='Buoyancy_flux_y'
               attrs['long_name']='Meridional Buoyancy flux'
               attrs['units']='m2/s3'
            if var == 'buoyancy_flux_z':
               attrs['standard_name']='Buoyancy_flux_x'
               attrs['long_name']='Vertical Buoyancy flux'
               attrs['units']='m2/s3'
        else:
            attrs=data_boxT.attrs
            attrs['standard_name']='Buoyancy'
            attrs['long_name']='Buoyancy'
            attrs['units']='m/s2'
        filt_data=filt(data_box)
        print('filtering of '+var+' ok')
    else:
        if var == 'vozocrtxSS' or var == 'vomecrtySS' or var == 'vovecrtzSS':
            if (int(date[4:6]) == 11 and int(date[6:9]) > 6) or (int(date[4:6]) > 11) or (int(date[0:4]) == 2010):
               filename = sorted(glob.glob(data_dir1+'a'+str(box)+'/1h/eNATL60a'+str(box)+'-BLBT02X_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_'+str(filetyps[var])+'.nc'))
            else:
               filename = sorted(glob.glob(data_dir+'a'+str(box)+'/1h/eNATL60a'+str(box)+'-BLBT02_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_'+str(filetyps[var])+'.nc'))
            file=filename[0]
            ds=xr.open_dataset(file,chunks={'time_counter':1,'x':1000,'y':1000})
            data_box=ds[str(var_help[var])][:,:,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
            attrs=data_box.attrs
            filt_data=filt(data_box)
        else: 
            if (int(date[4:6]) == 11 and int(date[6:9]) > 6) or (int(date[4:6]) > 11) or (int(date[0:4]) == 2010):
               filename = sorted(glob.glob(data_dir1+'a'+str(box)+'/1h/eNATL60a'+str(box)+'-BLBT02X_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_'+str(filetyps[var])+'.nc'))               
            else:
               filename = sorted(glob.glob(data_dir+'a'+str(box)+'/1h/eNATL60a'+str(box)+'-BLBT02_y'+str(date[0:4])+'m'+str(date[4:6])+'d'+str(date[6:9])+'.1h_'+str(filetyps[var])+'.nc'))
            print(filename)
            print(date)
            file=filename[0]
            ds=xr.open_dataset(file,chunks={'time_counter':1,'x':1000,'y':1000})
            data_box=ds[str(var)][:,:,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
            attrs=data_box.attrs
            filt_data=data_box - filt(data_box)
       
    dsgridh=xr.open_dataset(grid_dir+'/mesh_hgr_eNATL60a'+str(box)+'_3.6.nc',chunks={'x':1000,'y':1000})   
    e1=dsgridh[str(filee1[var])][0,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
    e2=dsgridh[str(filee2[var])][0,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
    dsgridz=xr.open_dataset(grid_dir+'/mesh_zgr_eNATL60a'+str(box)+'_3.6.nc',chunks={'x':1000,'y':1000})   
    e3=dsgridz[str(filee3[var])][0,:,jmin[ibox]-10:jmax[ibox]+10,imin[ibox]-10:imax[ibox]+10]
    e3t=e3.rename({'z':'deptht'})
    data_dx=dx_var(filt_data,e1)
    data_dy=dy_var(filt_data,e2)
    data_dz=dz_var(filt_data,e3t,filedeps[var])
    print('derivation of '+var+' ok')
    profile_data=filt_data[:,:,10:-10,10:-10].mean(dim={'x','y','time_counter'})
    profile_data_dx=data_dx[:,:,10:-10,10:-10].mean(dim={'x','y','time_counter'})
    profile_data_dy=data_dy[:,:,10:-10,10:-10].mean(dim={'x','y','time_counter'})
    profile_data_dz=data_dz[:,:,10:-10,10:-10].mean(dim={'x','y','time_counter'})
    print('averaging of '+var+' ok')
    return profile_data,profile_data_dx,profile_data_dy,profile_data_dz,attrs

def compute_all_profiles_all_var(date,ibox,imin,imax,jmin,jmax,box,box_name):
        dirb='/lus/scratch/CT1/hmg2840/aalbert/TMPEXTRACT/asommer/eNATL60/eNATL60-BLBT02-S/FiltredAveraged_Data2/'+str(box)
        profile_name=dirb+'/eNATL60'+str(box)+box_name[ibox]+'-BLBT02_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_predictors-profiles.nc'

        if not os.path.exists(dirb):
            os.makedirs(dirb)
        
        if not os.path.exists(profile_name):
            list_dataset=[]
            for var in ['buoyancy_flux_x','buoyancy_flux_y','buoyancy_flux_z']:

           #     dataset_name=dirb+'/eNATL60'+str(box)+box_name[ibox]+'-BLBT02_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_'+str(var)+'.nc'
           #     if not os.path.exists(dataset_name):
                    print('compute profile and dx,dy,dz of '+var)
                    profile_data,profile_data_dx,profile_data_dy,profile_data_dz,attrs=compute_all_profiles(var,date,ibox,imin,imax,jmin,jmax,box,box_name)
                    dataset=profile_data.to_dataset(name=var)
                    dataset[var].attrs=attrs
                    dataset[var].attrs['standard_name']=attrs['standard_name']
                    dataset[var].attrs['long_name']=attrs['long_name']
                    dataset[var].attrs['units']=attrs['units']
           #         print('writing netcdf for '+dataset_name)
           #         dataset.to_netcdf(path=dataset_name,mode='w')
                    list_dataset.append(dataset)
           #     dataset_name=dirb+'/eNATL60'+str(box)+box_name[ibox]+'-BLBT02_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_dx'+str(var)+'.nc'
           #     if not os.path.exists(dataset_name):
                    dataset=profile_data_dx.to_dataset(name='dx'+var)
                    dataset['dx'+var].attrs=attrs
                    dataset['dx'+var].attrs['standard_name']='dx gradient of '+attrs['standard_name']
                    dataset['dx'+var].attrs['long_name']='dx_'+attrs['long_name']
                    dataset['dx'+var].attrs['units']=attrs['units']
            #        print('writing netcdf for '+dataset_name)
            #        dataset.to_netcdf(path=dataset_name,mode='w')
                    list_dataset.append(dataset)

             #   dataset_name=dirb+'/eNATL60'+str(box)+box_name[ibox]+'-BLBT02_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_dy'+str(var)+'.nc'
             #   if not os.path.exists(dataset_name):
                    dataset=profile_data_dy.to_dataset(name='dy'+var)
                    dataset['dy'+var].attrs=attrs
                    dataset['dy'+var].attrs['standard_name']='dy gradient of '+attrs['standard_name']
                    dataset['dy'+var].attrs['long_name']='dy_'+attrs['long_name']
                    dataset['dy'+var].attrs['units']=attrs['units']
              #      print('writing netcdf for '+dataset_name)
              #      dataset.to_netcdf(path=dataset_name,mode='w')
                    list_dataset.append(dataset)

              #  dataset_name=dirb+'/eNATL60'+str(box)+box_name[ibox]+'-BLBT02_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_dz'+str(var)+'.nc'
              #  if not os.path.exists(dataset_name):
                    dataset=profile_data_dz.to_dataset(name='dz'+var)
                    dataset['dz'+var].attrs=attrs
                    dataset['dz'+var].attrs['standard_name']='dz gradient of '+attrs['standard_name']
                    dataset['dz'+var].attrs['long_name']='dz_'+attrs['long_name']
                    dataset['dz'+var].attrs['units']=attrs['units']
                    dataset_name=dirb+'/eNATL60'+str(box)+box_name[ibox]+'-BLBT02_y'+date[0:4]+'m'+date[4:6]+'d'+date[6:9]+'_dz'+str(var)+'.nc'
              #      print('writing netcdf for '+dataset_name)
              #      dataset.to_netcdf(path=dataset_name,mode='w')
                    list_dataset.append(dataset)

            print('merging all datasets')
            big_dataset=xr.merge(list_dataset)  
            big_dataset.attrs['global_attribute']= 'predictors profiles averaged over 24h and in '+box_name[ibox]+' computed on occigen '+str(today)
            print('writing to netcdf')
            big_dataset.to_netcdf(path=profile_name,mode='w')


## parser and main
def script_parser():
    """Customized parser.
    """
    from optparse import OptionParser
    usage = "usage: %prog box k[which box] date"
    parser = OptionParser(usage=usage)
    return parser

def main():
    parser = script_parser()
    (options, args) = parser.parse_args()
    if len(args) < 3: # print the help message if number of args is not 3.
        parser.print_help()
        sys.exit()
    optdic = vars(options)

    box = str(args[0])
    k = int(args[1])
    date = str(args[2])

    now=datetime.datetime.now()
    print("Start at ", now.strftime("%Y-%m-%d %H:%M:%S"))
    imin,imax,jmin,jmax,box_name=read_csv(box)

    compute_all_profiles_all_var(date,k,imin,imax,jmin,jmax,box,box_name)


    now=datetime.datetime.now()
    print("End at ", now.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    sys.exit(main() or 0)

