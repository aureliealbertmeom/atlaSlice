#!/usr/bin/env python

import sys, getopt, os, glob
import argparse
import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from functions import plots as pl
from functions import data as da
from functions import functions as f
from functions import calc as ca
from params import simulations_dict as params
from params import plots_dict as atlas

def parse_args():
    parser=argparse.ArgumentParser(description="all the plots")
    parser.add_argument('-mach',type=str,help='machine on which the plot is launched')
    parser.add_argument('-config',type=str,help='name of configuration')
    parser.add_argument('-simu',type=str,help='name of simulation')
    parser.add_argument('-var',type=str,help='name of variable')
    parser.add_argument('-reg',type=str,help='name of region')
    parser.add_argument('-typ',type=str,help='type of plot')
    parser.add_argument('-loc',type=str,help='location of plot')
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

    dirp=atlas.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(sim)


    print ('Plotting '+str(var)+' for configuration '+str(config))

    dirf=params.directory[machine][config][sim]

    if reg == config:
        files=glob.glob(dirf+'/'+str(config)+'_'+str(params.filetyp[sim][var])+'.nc')
    else:
        files=glob.glob(dirf+'/'+str(config)+str(reg)+'_'+str(params.filetyp[sim][var])+'.nc*')


    if len([name for name in files if os.path.isfile(name)]) == 1:

        plotname=dirp+'/'+str(config)+'-'+str(sim)+'_'+str(typ)+'_'+str(loc)+'_'+str(reg)+'_'+str(var)+'.png'

        if not os.path.isfile(plotname):
            filein=files[0]
            filemask = params.maskfile[machine][sim][reg]
            dsmask=xr.open_dataset(filemask)
            mask0=dsmask[f.maskname(params.vars_dim[var],params.filetyp[config][sim][var])][0]
            
            if loc == 'surf':
                var0=da.get_data2D_all_chunks(filein,params.vars_name[config][sim][var],-1)

            plottitle=str(config)+' '+atlas.vars_longname[var]
    
            if typ == 'map':
                lat0=dsmask['nav_lat']
                lon0=dsmask['nav_lon']
                if reg == 'npole' or reg == 'spole':
                    fig = plt.figure(figsize=(30,30))
                else:
                    if config in atlas.latlon_lim:
                        if reg in atlas.latlon_lims[config]:
                            nxx=np.abs(atlas.latlon_lims[config][reg][1]-atlas.latlon_lims[config][reg][0])
                            nyy=np.abs(atlas.latlon_lims[config][reg][3]-atlas.latlon_lims[config][reg][2])
                    else:

                    fig = plt.figure(figsize=(30,int(np.floor(30*nyy/nxx))))
    
                if reg == 'npole':
                    pl.one_map_proj_north_stereo(fig, 1, 1, 1, lon0, lat0, var0[t], atlas.vars_unit[var], mask0, atlas.vars_palette[var], atlas.vars_vlims[reg][var][0],atlas.vars_vlims[reg][var][1], plottitle)

                elif reg == 'spole':
                    pl.one_map_proj_south_stereo(fig, 1, 1, 1, lon0, lat0, var0[t], atlas.vars_unit[var], mask0, atlas.vars_palette[var], atlas.vars_vlims[reg][var][0],atlas.vars_vlims[reg][var][1], plottitle)

                else:
                    pl.one_map_proj_plate_carree_zoom(fig, 1, 1, 1, lon0, lat0, var0, atlas.vars_unit[var], mask0, atlas.vars_palette[var], atlas.vars_vlims[reg][var][0],atlas.vars_vlims[reg][var][1], plottitle,atlas.latlon_lims[config][reg][0],atlas.latlon_lims[config][reg][1],atlas.latlon_lims[config][reg][2],atlas.latlon_lims[config][reg][3])


            elif typ == 'map_noproj':
                nxx=atlas.xylims[config][reg][1]-atlas.xylims[config][reg][0]
                nyy=atlas.xylims[config][reg][3]-atlas.xylims[config][reg][2]
                fig = plt.figure(figsize=(30,int(np.floor(30*nyy/nxx))))

                pl.one_map_noproj_zoom(fig,1,1,1,var0[t],atlas.vars_unit[var],mask0,atlas.vars_palette[var],atlas.vars_vlims[reg][var][0],atlas.vars_vlims[reg][var][1],plottitle,atlas.xylims[config][reg][0],atlas.xylims[config][reg][1],atlas.xylims[config][reg][2],atlas.xylims[config][reg][3]);



            plt.savefig(plotname,bbox_inches='tight')
            plt.close()


if __name__ == "__main__":
    main()
