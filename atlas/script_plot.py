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

def parse_args():
    parser=argparse.ArgumentParser(description="all the plots")
    parser.add_argument('-mach',type=str,help='machine on which the plot is launched')
    parser.add_argument('-config',type=str,help='name of configuration')
    parser.add_argument('-simu',type=str,help='name of simulation')
    parser.add_argument('-var',type=str,help='name of variable')
    parser.add_argument('-reg',type=str,default='global',help='name of region')
    parser.add_argument('-typ',type=str,help='type of plot')
    parser.add_argument('-loc',type=str,default='surf',help='location of plot')
    parser.add_argument('-freq',type=str,help='frequency of variable')
    parser.add_argument('-date',type=str,help='date of file')
    parser.add_argument('-time',type=int,default=-1,help='time frame of file')
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
    ftime = parse_args().time

    dirp=params.scratch_path[machine]+'/'+str(config)+'/'+str(config)+'-'+str(sim)


    print ('Plotting '+str(var)+' for simulation '+str(config)+'-'+str(sim))

    dirf=params.directory[machine][config][sim]
    tag=f.tag_from_string_date(date,params.stylenom[machine][config][sim])

    if params.compute[var]==False:
        if params.stylenom[machine][config][sim] == '':
            files=glob.glob(dirf+'/*/'+str(freq)+'_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.filetyp[sim][var])+'.nc')
        elif params.stylenom[machine][config][sim] == 'dcm':
            files=glob.glob(dirf+'/'+str(freq)+'/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.filetyp[sim][var])+'.nc')
    else:
        files=glob.glob(dirf+'/*/'+str(freq)+'_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][0])+'.nc')

    if len([name for name in files if os.path.isfile(name)]) == 1:

        filein=files[0]
        filemask = params.maskfile[machine][sim]
        dsmask=xr.open_dataset(filemask)
        mask0=dsmask[f.maskname(params.vars_dim[var],params.filetyp[sim][var])][0]
        dst=xr.open_dataset(filein)
        ttime=dst.time_counter
        if ftime > -1:
            lent=1
        else:
            lent=len(ttime)
        dstt=xr.open_dataset(filein,decode_cf=False)
        timetag=dstt.time_counter.values

        #Retrieve the right variable and mask parameters

        if typ[:3] == 'map':

            if typ != 'map_noproj':
                lat0=dsmask['nav_lat']
                lon0=dsmask['nav_lon']

            if loc == 'surf':
                if params.compute[var]==False:
                    var0=da.get_data2D_all_chunks(filein,params.vars_name[sim][var],-1)
                else:
                    filein1=files[0]
                    files2=glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][1])+'.nc')
                    filein2=files2[0]
                    var0=da.get_compute_2var2D_all_chunks(filein1,filein2,var,params.compute_varname[sim][var][0],params.compute_varname[sim][var][1],filemask,-1)

            if loc == '1000m':
                if params.compute[var]==False:
                    var0=da.get_data2D_all_chunks(filein,params.vars_name[sim][var],params.lev[config][loc])
                else:
                    filein1=files[0]
                    files2=glob.glob(dirf+'/*/1h_OUTPUT/'+str(config)+'-'+str(sim)+'_'+str(tag)+'.'+str(freq)+'_'+str(params.compute_filetyp[sim][var][1])+'.nc')
                    filein2=files2[0]
                    var0=da.get_compute_2var2D_all_chunks(filein1,filein2,var,params.compute_varname[sim][var][0],params.compute_varname[sim][var][1],filemask,params.lev[config][loc])

        if typ == 'section':
            var0=da.get_data3D(filein,params.vars_name[sim][var])
            lat0=dsmask['nav_lat']
            lon0=dsmask['nav_lon']
            dep0=dsmask['nav_lev']

        if typ == 'zyplot':
            var0=da.get_data3D(filein,params.vars_name[sim][var])
            lat0=da.get_data3D(filein,'nav_lat')
            dep0=dsmask['nav_lev']

        #Loop over the time steps contained in the file
        for t in np.arange(lent):
            if lent==1:
                t=ftime
            print('Plotting for t='+str(ttime[t].values))
            if typ == 'zyplot':
                plotname=dirp+'/'+str(config)+'-'+str(sim)+'_'+str(typ)+'_'+str(reg)+'_'+str(tag)+'.'+str(freq)+'_'+str(var)+'_t'+str(int(timetag[t]))+'.png'
            else:
                plotname=dirp+'/'+str(config)+'-'+str(sim)+'_'+str(typ)+'_'+str(loc)+'_'+str(reg)+'_'+str(tag)+'.'+str(freq)+'_'+str(var)+'_t'+str(int(timetag[t]))+'.png'
            if not os.path.isfile(plotname):
                if typ[:3] == 'map':
                    if reg == 'npole' or reg == 'spole':
                        fig = plt.figure(figsize=(30,30))
                    else:
                        nxx=params.xylims[config][reg][1]-params.xylims[config][reg][0]
                        nyy=params.xylims[config][reg][3]-params.xylims[config][reg][2]
                        fig = plt.figure(figsize=(30,int(np.floor(30*nyy/nxx))))
                    plottitle=str(config)+'-'+str(sim)+' '+params.vars_longname[var]+' '+str(pd.to_datetime(str(ttime[t].values)).strftime('%Y-%m-%d %H:%M'))
                    if typ == 'map_noproj':
                        pl.one_map_noproj_zoom(fig,1,1,1,var0[t],params.vars_unit[var],mask0,params.vars_palette[var],params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],plottitle,params.xylims[config][reg][0],params.xylims[config][reg][1],params.xylims[config][reg][2],params.xylims[config][reg][3]);

                    if typ == 'map_stereo':

                        if reg == 'npole':
                            pl.one_map_proj_north_stereo(fig, 1, 1, 1, lon0, lat0, var0[t], params.vars_unit[var], mask0, params.vars_palette[var], params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1], plottitle)

                        if reg == 'spole':
                            pl.one_map_proj_south_stereo(fig, 1, 1, 1, lon0, lat0, var0[t], params.vars_unit[var], mask0, params.vars_palette[var], params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1], plottitle)

                    if typ == 'map_orthoa':
                            pl.one_map_proj_ortho_global(fig, 1, 1, 1, lon0, lat0, var0[t], params.vars_unit[var], mask0, params.vars_palette[var], params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1], plottitle,30,-30)

                    if typ == 'map_orthop':
                            pl.one_map_proj_ortho_global(fig, 1, 1, 1, lon0, lat0, var0[t], params.vars_unit[var], mask0, params.vars_palette[var], params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1], plottitle,10,-165)

                    if typ == 'map_moll':
                            pl.one_map_proj_mollweide_global(fig, 1, 1, 1, lon0, lat0, var0[t], params.vars_unit[var], mask0, params.vars_palette[var], params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1], plottitle)

                if typ == 'section':
                    nxx=params.sections_coords[config][loc][2]-params.sections_coords[config][loc][1]
                    nyy=params.sections_deplim[loc]
                    fig = plt.figure(figsize=(30,np.max([10,int(np.floor(3*nyy/nxx))])))
                    if params.sections_orientation[loc] == 'lat':
                        plottitle=str(config)+'-'+str(sim)+' section of '+params.vars_longname[var]+' at lat='+str(lat0[params.sections_coords[config][loc][0],params.sections_coords[config][loc][1]].values)+' for '+str(ttime[t].values)
                        ax=fig.add_subplot(111)
                        pl.sections_latitude(ax,params.sections_coords[config][loc][0],params.sections_coords[config][loc][1],params.sections_coords[config][loc][2],var0,mask0,lon0,dep0,params.vars_palette[var],params.sections_deplim[loc],params.vars_vlims[loc][var][0],params.vars_vlims[loc][var][1],params.vars_unit[var],plottitle)
                    if params.sections_orientation[loc] == 'lon':
                        plottitle=str(config)+'-'+str(sim)+' section of '+params.vars_longname[var]+' at lon='+str(lon0[params.sections_coords[config][loc][1],params.sections_coords[config][loc][0]].values)+' for '+str(ttime[t].values)
                        ax=fig.add_subplot(111)
                        pl.sections_longitude(ax,params.sections_coords[config][loc][0],params.sections_coords[config][loc][1],params.sections_coords[config][loc][2],var0,mask0,lat0,dep0,params.vars_palette[var],params.sections_deplim[loc],params.vars_vlims[loc][var][0],params.vars_vlims[loc][var][1],params.vars_unit[var],plottitle)

                if typ == 'zyplot':
                    fig = plt.figure(figsize=(30,20))
                    plottitle=str(config)+'-'+str(sim)+' section of '+params.vars_longname[var]+' in '+str(reg)+' for '+str(ttime[t].values)
                    pl.plot_zy(fig,dep0,lat0,var0[t],params.vars_vlims[reg][var][0],params.vars_vlims[reg][var][1],params.vars_unit[var], params.vars_palette[var],plottitle)
                plt.savefig(plotname)
                plt.close()


if __name__ == "__main__":
    main()
