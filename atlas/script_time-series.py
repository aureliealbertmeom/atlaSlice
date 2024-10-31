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

    machine = 'adastra'
    config = 'eORCA36.L121'
    sim = 'EXP15-10'
    var = 'SSH'
    reg = 'global'
    typ = 'time_series'
    loc = 'surf'
    freq = '1h'
    date_init = '2012-01-01 11:00'
    date_end = '2012-02-22 23:00'

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

    # Get the path and expected plotname
    dirp=params.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(sim)
    dirf=params.directory[machine][config][sim]
    plotname=dirp+'/'+str(config)+'-'+str(sim)+'_'+str(typ)+'_'+str(loc)+'_'+str(reg)+'_'+str(f.tag_from_string_date(date_init,params.stylenom[machine][config][sim]))+'-'+str(f.tag_from_string_date(date_end,params.stylenom[machine][config][sim]))+'.'+str(freq)+'_'+str(var)+'.png'

    #If the plot has already been produced it is not done again
    if not os.path.isfile(plotname):
        print ('Plotting '+str(typ)+' '+str(var)+' for simulation '+str(config)+'-'+str(sim))

        #Get the dates for the whole period
        if date_init == date_end:
            all_dates=[pd.Timestamp(date_init)]
        else:
            all_dates=pd.date_range(date_init,date_end,freq=params.frequencies_file[sim][var])
    
        #Create empty time and var fields
        total_time = np.empty((0,0))
        if typ == 'hovmuller':
            nxx=params.xylims[config][reg][1]-params.xylims[config][reg][0]
            nyy=params.xylims[config][reg][3]-params.xylims[config][reg][2]
            if nxx > 1:
                total_var = np.empty((0,nxx+1))
            else:
                total_var = np.empty((0, nyy+1))
        else:
            total_mean_var = np.empty((0, 0))
            total_min_var = np.empty((0, 0))
            total_max_var = np.empty((0, 0))

        #Make a loop on the date and fill the time and var fields for the whole period
        for date in all_dates:
            tag=f.tag_from_string_date(date,params.stylenom[machine][config][sim])

            #Get the file name, depending on the variable to get or compute
            if params.compute[var]==False:
                files=glob.glob(dirf+'/*/'+str(freq)+'_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.filetyp[sim][var])+'.nc')
            else:
                files=glob.glob(dirf+'/*/'+str(freq)+'_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][0])+'.nc')

            #We should deal with one file at the time
            if len([name for name in files if os.path.isfile(name)]) == 1:

                filein=files[0]
                filemask = params.maskfile[machine][sim]
                #Retrieve the time variable, not as a datetime
                dstt=xr.open_dataset(filein,decode_cf=False)
                append_time=dstt.time_counter.values
                total_time=np.append(total_time,append_time)

                if loc == 'surf' and params.vars_dim[var] == '2D':
                    if params.compute[var] == False:
                        var0=da.get_mdata2D_all_chunks(filein,params.vars_name[sim][var],-1,filemask,f.maskname(params.vars_dim[var],params.filetyp[sim][var]))
                    else:
                        filein1=files[0]
                        files2=glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][1])+'.nc')
                        filein2=files2[0]
                        var0=da.get_compute_2var2D_all_chunks(filein1,filein2,var,params.compute_params.vars_name[sim][var][sim][var][0],params.compute_params.vars_name[sim][var][sim][var][1],filemask,-1)

                    if typ == 'time_series':
                        tvar0=var0[:,params.xylims[config][reg][2]:params.xylims[config][reg][3],params.xylims[config][reg][0]:params.xylims[config][reg][1]].squeeze()
                        append_mean_var=tvar0.mean(dim=["x", "y"])
                        total_mean_var=np.append(total_mean_var,append_mean_var)
                        append_min_var=tvar0.min(dim=["x", "y"])
                        total_min_var=np.append(total_min_var,append_min_var)
                        append_max_var=tvar0.max(dim=["x", "y"])
                        total_max_var=np.append(total_max_var,append_max_var)

                    if typ == 'hovmuller':
                        append_var=var0[:,params.xylims[config][reg][2]:params.xylims[config][reg][3]+1,params.xylims[config][reg][0]:params.xylims[config][reg][1]+1].squeeze()
                        total_var=np.append(total_var,append_var, axis=0)

        #Make the plot
        fig = plt.figure(figsize=(30,30))
        plottitle=str(config)+'-'+str(sim)+' '+str(reg)+' '+str(loc)+' '+str(typ)+' of '+params.vars_longname[var]

        if typ == 'time_series':
            pl.plot_time_series_min_max(fig,pd.to_datetime(total_time, unit='s', origin='1800-01-01'),total_mean_var,total_min_var,total_max_var,params.vars_unit[var],plottitle);
        if typ == 'hovmuller':
            real_time,real_var=f.real_time_data2D(total_time,total_var)
            if params.xylims[config][reg][1]-params.xylims[config][reg][0] > 1:
                lon=da.get_data2D_all_chunks(params.maskfile[machine][sim],'glamt',-1)
                lon0=lon[params.xylims[config][reg][2]:params.xylims[config][reg][3]+1,params.xylims[config][reg][0]:params.xylims[config][reg][1]+1].squeeze()
                pl.plot_hovmuller_lon(fig,pd.to_datetime(real_time, unit='s', origin='1800-01-01'),lon0.values,real_var,params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],params.vars_unit[var],params.vars_palette[var],plottitle);
            else:
                lat=da.get_data2D_all_chunks(params.maskfile[machine][sim],'gphit',-1)
                lat0=lat[params.xylims[config][reg][2]:params.xylims[config][reg][3]+1,params.xylims[config][reg][0]:params.xylims[config][reg][1]+1].squeeze()
                pl.plot_hovmuller_lat(fig,pd.to_datetime(total_time, unit='s', origin='1800-01-01'),lat0.values,total_var,params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],params.vars_unit[var],params.vars_palette[var],plottitle);

        plt.savefig(plotname,bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    main()
