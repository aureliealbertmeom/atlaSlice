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
    parser.add_argument('-date',type=str,help='date of file')
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
    date = parse_args().date

    dirp=params.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(sim)
    if not os.path.isdir(dirp):
        os.makedirs(dirp)


    print ('Plotting '+str(var)+' for simulation '+str(config)+'-'+str(sim))

    dirf=params.directory[machine][config][sim]
    tag=f.tag_from_string_date(date,params.stylenom[machine][config][sim])

    if len([name for name in glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.filetyp[sim][var])+'.nc') if os.path.isfile(name)]) == 1:
            filein=glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.filetyp[sim][var])+'.nc')[0]

            filemask = params.maskfile[machine][sim]
            dsmask=xr.open_dataset(filemask)

            dst=xr.open_dataset(filein)
            ttime=dst.time_counter
            lent=len(ttime)
            dstt=xr.open_dataset(filein,decode_cf=False)
            timetag=dstt.time_counter.values
            mask0=dsmask[f.maskname(params.vars_dim[var],params.filetyp[sim][var])][0]
            if loc == 'surf':
                var0=da.get_data2D_all_chunks(filein,params.vars_name[sim][var],-1)
                for t in np.arange(lent):
                    print('Plotting for t='+str(ttime[t].values))
                    if typ == 'map_noproj':
                        plotname=dirp+'/'+str(config)+'-'+str(sim)+'_'+str(typ)+'_'+str(loc)+'_'+str(reg)+'_'+str(tag)+'.'+str(freq)+'_'+str(var)+'_t'+str(int(timetag[t]))+'.png'
                        if not os.path.isfile(plotname):
                            nxx=params.xylims[config][reg][1]-params.xylims[config][reg][0]
                            nyy=params.xylims[config][reg][3]-params.xylims[config][reg][2]
                            fig = plt.figure(figsize=(30,int(np.floor(30*nyy/nxx))))
                            plottitle=str(config)+'-'+str(sim)+' '+params.vars_longname[var]+' '+str(ttime[t].values)
                            pl.one_map_noproj_zoom(fig,1,1,1,var0[t],params.vars_unit[var],mask0,params.vars_palette[var],params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],plottitle,params.xylims[config][reg][0],params.xylims[config][reg][1],params.xylims[config][reg][2],params.xylims[config][reg][3]);
                            plt.savefig(plotname)
                            plt.close()


if __name__ == "__main__":
    main()
