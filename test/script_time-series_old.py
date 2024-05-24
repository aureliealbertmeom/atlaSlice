#!/usr/bin/env python

import sys, getopt, os, glob
import argparse
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from atlas import plots as pl
from atlas import data as da
from atlas import functions as f
from atlas import calc as ca
from params import simulations_dict as params

def parse_args():
    parser=argparse.ArgumentParser(description="all the plots")
    parser.add_argument('-mach',type=str,help='machine on which the plot is launched')
    parser.add_argument('-config',type=str,help='name of configuration')
    parser.add_argument('-simu',type=str,help='name of simulation')
    parser.add_argument('-var',type=str,help='name of variable')
    parser.add_argument('-reg',type=str,help='name of region')
    parser.add_argument('-typ',type=str,help='type of plot')
    parser.add_argument('-loc',type=str,help='location of plot')
    parser.add_argument('-freq',type=str,help='frequency of variable')
    parser.add_argument('-date_init',type=str,help='initial date of period')
    parser.add_argument('-date_end',type=str,help='end date of period')
    args=parser.parse_args()
    return args

def main():
    machine = parse_args().mach
    config = parse_args().config
    sim = parse_args().simu
    var = parse_args().var
    reg = parse_args().reg
    typ = parse_args().typ
    loc = parse_args().loc
    freq = parse_args().freq
    date_init = parse_args().date_init
    date_end = parse_args().date_end

    dirp=params.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(sim)
    dirf=params.directory[machine][config][sim]

    total_time = np.empty((0,0))
    total_var = np.empty((0,0))

    #Make a loop on the date
    if date_init == date_end:
        all_dates=[pd.Timestamp(date_init)]
    else:
        all_dates=pd.date_range(date_init,date_end,freq=params.frequencies_file[sim][var])

    if typ == 'time_series':
        print ('Plotting time series '+str(var)+' for simulation '+str(config)+'-'+str(sim))
        total_mean_var = np.empty((0, 0))
        total_min_var = np.empty((0, 0))
        total_max_var = np.empty((0, 0))
    if typ == 'hovmuller':
        print ('Plotting hovmuller '+str(var)+' for simulation '+str(config)+'-'+str(sim))
        nxx=params.xylims[config][reg][1]-params.xylims[config][reg][0]
        nyy=params.xylims[config][reg][3]-params.xylims[config][reg][2]
        if nxx > 1:
            total_var = np.empty((0, nxx+1))
        else:
            total_var = np.empty((0, nyy+1))

    for date in all_dates:
        tag=f.tag_from_string_date(date,params.stylenom[machine][config][sim])

        if params.compute[var]==False:
            files=glob.glob(dirf+'/*/'+str(freq)+'_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.filetyp[sim][var])+'.nc')
        else:
            files=glob.glob(dirf+'/*/'+str(freq)+'_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][0])+'.nc')

        if len([name for name in files if os.path.isfile(name)]) == 1:

            filein=files[0]
            filemask = params.maskfile[machine][sim]
            dsmask=xr.open_dataset(filemask)
            mask0=dsmask[f.maskname(params.vars_dim[var],params.filetyp[sim][var])][0]
            dst=xr.open_dataset(filein)
            ttime=dst.time_counter
            lent=len(ttime)
            dstt=xr.open_dataset(filein,decode_cf=False)
            timetag=dstt.time_counter.values
            total_time=np.append(total_time,timetag)

            if loc == 'surf' and params.vars_dim[var] == '2D':
                if params.compute[var]==False:
                    var0=da.get_data2D_all_chunks(filein,params.vars_name[sim][var],-1)
                else:
                    filein1=files[0]
                    files2=glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][1])+'.nc')
                    filein2=files2[0]
                    var0=da.get_compute_2var2D_all_chunks(filein1,filein2,var,params.compute_varname[sim][var][0],params.compute_varname[sim][var][1],filemask,-1)

                if typ == 'time_series':
                    tvar0=var0[:,params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]]
                    tmask0=mask0[params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]]
                    var0m=np.ma.array(tvar0,mask=1-tmask0)
                    mean_var=var0m.mean(dim=["x", "y"])
                    min_var=var0m.min(dim=["x", "y"])
                    max_var=var0m.max(dim=["x", "y"])
                if typ == 'hovmuller':
                    if nxx > 1:
                        lon0=dsmask['nav_lon'][params.xylims[config][reg][2]:params.xylims[config][reg][3]+1,params.xylims[config][reg][0]:params.xylims[config][reg][1]+1]
                    else:
                        lat0=dsmask['nav_lat'][params.xylims[config][reg][2]:params.xylims[config][reg][3]+1,params.xylims[config][reg][0]:params.xylims[config][reg][1]+1]
                    hov_var=var0[:,params.xylims[config][reg][2]:params.xylims[config][reg][3]+1,params.xylims[config][reg][0]:params.xylims[config][reg][1]+1]
                    tmask0=mask0[params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]]
                    hov_varm=np.ma.array(hov_var,mask=1-tmask0)
            
            if loc == '3D':
                if params.compute[var]==False:
                    var0=da.get_data3D(filein,params.vars_name[sim][var])
                else:
                    filein1=files[0]
                    files2=glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][1])+'.nc')
                    filein2=files2[0]
                    var0=da.get_compute_2var3D_all_chunks(filein1,filein2,var,params.compute_varname[sim][var][0],params.compute_varname[sim][var][1],filemask)
                if typ == 'time_series':
                    tvar0=var0[:,:,params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]]
                    var0m=np.ma.array(tvar0,mask=1-mask)
                    mean_var=var0[:,:,params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]].mean(dim=["x", "y",params.depnam[var]])
                    min_var=var0[:,:,params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]].min(dim=["x", "y",params.depnam[var]])
                    max_var=var0[:,:,params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]].max(dim=["x", "y",params.depnam[var]])
            
            if typ == 'time_series':
                total_mean_var=np.append(total_mean_var,mean_var.values)
                total_min_var=np.append(total_min_var,min_var.values)
                total_max_var=np.append(total_max_var,max_var.values)
            if typ == 'hovmuller':
                total_var=np.append(total_var,hov_varm.values.squeeze(), axis=0)

    if typ == 'hovmuller':
        real_time,real_var=f.real_time_data2D(total_time,total_var)
    print('Plotting for var ='+str(var))
#    np.set_printoptions(threshold=sys.maxsize)
#    print('check total time :',np.diff(total_time))
#    np.set_printoptions(threshold=1000)

    plotname=dirp+'/'+str(config)+'-'+str(sim)+'_'+str(typ)+'_'+str(loc)+'_'+str(reg)+'_'+str(f.tag_from_string_date(date_init,params.stylenom[machine][config][sim]))+'-'+str(f.tag_from_string_date(date_end,params.stylenom[machine][config][sim]))+'.'+str(freq)+'_'+str(var)+'.png'
    if not os.path.isfile(plotname):
        fig = plt.figure(figsize=(30,30))
        if typ == 'time_series':
            plottitle=str(config)+'-'+str(sim)+' '+str(reg)+' '+str(loc)+' mean, max and min of '+params.vars_longname[var]
            pl.plot_time_series_min_max(fig,pd.to_datetime(total_time, unit='s', origin='1800-01-01'),total_mean_var,total_min_var,total_max_var,params.vars_unit[var],plottitle);
        if typ == 'hovmuller':
            plottitle=str(config)+'-'+str(sim)+' '+str(reg)+' '+str(loc)+' hovmuller of '+params.vars_longname[var]
            if nxx > 1:
                pl.plot_hovmuller_lon(fig,pd.to_datetime(real_time, unit='s', origin='1800-01-01'),lon0.squeeze(),real_var,params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],params.vars_unit[var],params.vars_palette[var],plottitle);
            else:
                pl.plot_hovmuller_lat(fig,pd.to_datetime(real_time, unit='s', origin='1800-01-01'),lat0.squeeze(),real_var,params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],params.vars_unit[var],params.vars_palette[var],plottitle);

        plt.savefig(plotname,bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    main()
