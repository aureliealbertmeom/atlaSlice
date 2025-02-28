#! /usr/bin/env python

import sys,getopt,os,glob
import argparse
import pandas as pd
import shutil
import subprocess
import numpy as np

#Make sure the path to the package is in the PYTHONPATH
from functions import functions as f
from params import simulations_dict as params
from params import slice_dict as sliced

da = __import__('ANNA60-BLBT02-1h-3D-W')


machine=da.machine;configuration=da.configuration;simulations=da.simulations;regions=da.regions;variables=da.variables;frequency=da.frequency;date_init=da.date_init;date_end=da.date_end;operation=da.operation


#Check wether the desired outputs have been produced
simulation=simulations[0]
region=regions[0]

nb_month=0
nb_day=0

var=variables[0]

#Depending on the operation the outputs are poduced in different directories
if operation == 'extract':
    tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
if operation[:6] == 'degrad':
    tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'-'+str(operation)+'/'+str(frequency)

if params.frequencies_file[configuration][simulation][var]=='1d':
    all_day=pd.date_range(date_init,date_end,freq='D')
    err=0
    for dm in all_day:
        tag=f.tag_from_panda_day(dm)
        filed=tdir+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_'+str(tag)+'.'+str(frequency)+'_'+str(var)+'.nc'
        if not os.path.exists(filed):
            err=err+1
            print('file '+str(filed)+' is missing')
    if err > 0:
        print('A total of '+str(err)+' are missing, dataset is not complete')
    else:
        print('No missing files, dataset is complete')

if params.frequencies_file[configuration][simulation][var]=='1m':
    all_month=pd.date_range(date_init,date_end,freq='M')
    err=0
    for month in all_month:
        tag=f.tag_from_panda_month(month)
        filed=tdir+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_'+str(tag)+'.'+str(frequency)+'_'+str(var)+'.nc'
        if not os.path.exists(filed):
            err=err+1
            print('file '+str(filed)+' is missing')
    if err > 0:
        print('A total of '+str(err)+' are missing, dataset is not complete')
    else:
        print('No missing files, dataset is complete')

mpmdname='tmp_make_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'

if operation == 'extract':
    if params.vars_dim[var]=='2D':
        print('We are going to archive variable '+str(var)+' year by year')
        freq_par='1y'
    if params.vars_dim[var]=='3D':
        print('We are going to archive variable '+str(var)+' month by month')
        freq_par='1m'
if operation[:6] == 'degrad':
    print('We are going to archive variable '+str(var)+' year by year')
    freq_par='1y'

if freq_par == '1y':
    all_month=pd.date_range(date_init,date_end,freq='M')
    yeari=all_month[0].year
    yearf=all_month[-1].year
    for year in np.arange(yeari,yearf+1):
        if operation == 'extract':
            tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
            tarname=str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'.'+str(frequency)+'_'+str(var)+'-'+str(operation)+'.tar'
            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(year)+'.ksh'
            f.use_template('script_save_2Dvar_1year_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})
        if operation[:6] == 'degrad':
            tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'-'+str(operation)+'/'+str(frequency)
            tarname=str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'.'+str(frequency)+'_'+str(var)+'-'+str(operation)+'.tar'
            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'-'+str(operation)+'_'+str(frequency)+'_'+str(year)+'.ksh'
            f.use_template('script_save_2Dvar_1year_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var)+'-'+str(operation),'FREQUENCY':str(frequency), 'YEAR':str(year), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})

if freq_par == '1m':
    all_month=pd.date_range(date_init,date_end,freq='M')
    for ym in all_month:
        year=ym.year
        month=ym.month
        mm="{:02d}".format(month)
        if operation == 'extract':
            tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
            tarname=str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'.'+str(frequency)+'_'+str(var)+'.tar'
            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'-'+str(operation)+'_'+str(frequency)+'_'+str(year)+str(mm)+'.ksh'
            f.use_template('script_save_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year),'MONTH':str(mm), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})
        if operation[:6] == 'degrad':
            tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'-'+str(operation)+'/'+str(frequency)
            tarname=str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'.'+str(frequency)+'_'+str(var)+'-'+str(operation)+'.tar'
            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'-'+str(operation)+'_'+str(frequency)+'_'+str(year)+str(mm)+'.ksh'
            f.use_template('script_save_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var)+'-'+str(operation),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})

subprocess.call(["chmod", "+x", savename])
with open(mpmdname, 'a') as file:
    file.write("{}\n".format(' ./'+str(savename)))
    
print('We are going to run the scripts on the frontal node')
subprocess.call(["chmod", "+x", mpmdname])
subprocess.run(sliced.script_path[machine]+'/'+mpmdname,shell=True)
