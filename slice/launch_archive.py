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

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated job")
    parser.add_argument('-param',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check_output_1sim_1reg(machine,configuration,simulation,region,variables,frequency,date_init,date_end,operation):
    
    #Check wether the desired outputs have been produced
    for var in variables:
        if params.frequencies_file[configuration][simulation][var]=='1d':
            all_day=pd.date_range(date_init,date_end,freq='D')
            err=0
            for dm in all_day:
                tag=f.tag_from_panda_day(dm)
                if operation == 'extract':
                    tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
                    filed=tdir+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_'+str(tag)+'.'+str(frequency)+'_'+str(var)+'.nc'
                    if not os.path.exists(filed):
                        err=err+1
                        print('file '+str(filed)+' is missing')
            if err > 0:
                print('A total of '+str(err)+' of '+str(var)+' files  are missing, dataset is not complete')
            else:
                print('No missing files, dataset is complete for var '+str(var))
        if params.frequencies_file[configuration][simulation][var]=='1m':
            all_month=pd.date_range(date_init,date_end,freq='M')
            err=0
            for month in all_month:
                tag=f.tag_from_panda_month(month)
                if operation == 'extract':
                    tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
                    filed=tdir+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_'+str(tag)+'.'+str(frequency)+'_'+str(var)+'.nc'  
                    if not os.path.exists(filed):
                        err=err+1
                        print('file '+str(filed)+' is missing')
            if err > 0:
                print('A total of '+str(err)+' of '+str(var)+' files are missing, dataset is not complete')
            else:
                print('No missing files, dataset is complete for var '+str(var))

def check_output(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):
    #For all simulations, regions and variables
    for simulation in simulations:
        for region in regions:
            check_output_1sim_1reg(machine,configuration,simulation,region,variables,frequency,date_init,date_end,operation)


def make_archive_1sim_1reg_1var(machine,configuration,simulation,region,var,frequency,date_init,date_end,operation):
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
    return savename


def set_up_all_scripts(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):

    list_scripts=[]

    for simulation in simulations:
        for region in regions:
            for var in variables:
                savename=make_archive_1sim_1reg_1var(machine,configuration,simulation,region,var,frequency,date_init,date_end,operation)
                list_scripts.append(savename)

    return list_scripts

def run_all_scripts(list_scripts,machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation,job):
    #Concatenate the name of all simulations and regions
    allregions=f.concatenate_all_names_in_list(regions)
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allvariables=f.concatenate_all_names_in_list(variables)

    #The scripts are run sequentially on the frontal node
    if job == 'N':
        master_script='tmp_ms_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
        for script in list_scripts:
            with open(master_script, 'a') as file:
                file.write("{}\n".format(' ./'+str(script)))
        subprocess.call(["chmod", "+x", master_script])
        subprocess.run(sliced.script_path[machine]+'/'+master_script,shell=True)

    #The scripts are distributed in mpdm files and will be run in parallel
    else:
        #Get the maximum number of parallel scripts that can run in parallel on one node
        if operation[:6] == 'degrad':
            nb_proc_max=sliced.mprocs[operation[:6]]
        else:
            nb_proc_max=sliced.mprocs[operation]
        #Name of the first mpmd and job file
        mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
        jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
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
                subprocess.call(["sbatch",jobname])

                #The next job is set up
                nb_jobs=nb_jobs+1
                nb_procs=0
                mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                jobname='tmp_job'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

        if nb_procs > 0:
            #The last job is launched
            subprocess.call(["chmod", "+x", mpmdname])
            subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
            subprocess.call(["sbatch",jobname])



def main():
    param_dataset = parse_args().param
    da = __import__(param_dataset)

    print('Checking the number of files produced for operation '+str(da.operation)+' for '+str(param_dataset))
    check_output(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
    list_scripts=set_up_all_scripts(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
    run_all_scripts(list_scripts,da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation,da.job)

if __name__ == "__main__":
    main()
