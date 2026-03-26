#! /usr/bin/env python

import sys,getopt,os, glob
import argparse
import pandas as pd
import shutil
import subprocess
import datetime
from calendar import monthrange
import numpy as np

#Make sure the path to the package is in the PYTHONPATH
from functions import functions as f
from params import simulations_dict as params
from params import slice_dict as sliced

da = __import__('OCCIPUT-bot-pres')

machine=da.machine;configuration=da.configuration;simulations=da.simulations;regions=da.regions;variables=da.variables;frequency=da.frequency;date_init=da.date_init;date_end=da.date_end;operation=da.operation

list_scripts=[]

var=variables[0]

print('We are going to archive variable '+str(var)+' month by month')
freq_par='1m'
incr_temp=pd.date_range(date_init,date_end,freq='M')

for ym in incr_temp:
    year=ym.year
    month=ym.month
    mm="{:02d}".format(month)
    tag=str(year)+'-'+str(mm)

    for simulation in simulations:
        region=regions[0]

        scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
        compute_var=operation[8:]

        outputname=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'-S/'+str(frequency)+'/'+str(region)+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'.'+str(frequency)+'_'+str(compute_var)+'.nc'

        f.use_template('script_'+str(operation)+'_3Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'SOURCEDIR':str(params.directory[machine][configuration][simulation]),'SCPATH':str(sliced.scratch_path[machine]),'CDFPATH':str(sliced.cdf_path[machine]),'MASKFILE':str(params.maskfile[machine][configuration][region]),'MESHHFILE':str(params.mesh_hgr[machine][configuration][region]),'MESHZFILE':str(params.mesh_zgr[machine][configuration][region])})
        subprocess.call(["chmod", "+x", scriptname])
        list_scripts.append(scriptname)

allregions=f.concatenate_all_names_in_list(regions)
allsimulations=f.concatenate_all_names_in_list(simulations)
allvariables=f.concatenate_all_names_in_list(variables)
allmembers=''

nb_proc_max=sliced.mprocs[operation]

mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(allmembers)+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(allmembers)+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

nb_procs=0
nb_jobs=1
for script in list_scripts:
            with open(mpmdname, 'a') as file:
                file.write("{}\n".format(str(nb_procs)+' ./'+str(script)))
            nb_procs=nb_procs+1
            if nb_procs == nb_proc_max:
                #The job is launched
                subprocess.call(["chmod", "+x", mpmdname])
                subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])

                #The next job is set up
                nb_jobs=nb_jobs+1
                nb_procs=0
                mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(allmembers)+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                jobname='tmp_job'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(allmembers)+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

if nb_procs > 0:
            #The last job is launched
            subprocess.call(["chmod", "+x", mpmdname])
            subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])

