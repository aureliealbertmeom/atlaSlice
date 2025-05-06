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

def make_script_archive_1sim_1typ_1day(machine,configuration,simulation,typ,frequency,year,mm,dd,inplace):

    tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(configuration)+'-'+str(simulation)+'-S'
    tarname=str(configuration)+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'d'+str(dd)+'.'+str(frequency)+'_'+str(typ)+'.tar'
    savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(typ)+'_'+str(frequency)+'_'+str(year)+str(mm)+str(dd)+'.ksh'
    f.use_template('script_save_output_3Dvar_1day_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'VARIABLE':str(typ),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine]),'YON':inplace,'STYLENOM':params.stylenom[machine][configuration][simulation]})
    subprocess.call(["chmod", "+x", savename])
    return savename

def make_script_archive_1sim_1typ_1month(machine,configuration,simulation,typ,frequency,year,mm,inplace):

    tdir=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(configuration)+'-'+str(simulation)+'-S'
    tarname=str(configuration)+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'.'+str(frequency)+'_'+str(typ)+'.tar'
    savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(typ)+'_'+str(frequency)+'_'+str(year)+str(mm)+'.ksh'
    f.use_template('script_save_output_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'VARIABLE':str(typ),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine]),'YON':inplace,'STYLENOM':params.stylenom[machine][configuration][simulation]})
    subprocess.call(["chmod", "+x", savename])
    return savename

def set_up_all_scripts(machine,configuration,simulations,variables,frequency,date_init,date_end,inplace):

    list_scripts=[]

    for simulation in simulations:
            for var in variables:
                if var == 'icemod':
                    all_day=pd.date_range(date_init,date_end,freq='D')
                    for dm in all_day:
                            year=dm.year
                            month=dm.month
                            day=dm.day
                            mm="{:02d}".format(month)
                            dd="{:02d}".format(day)
                            savename=make_script_archive_1sim_1typ_1day(machine,configuration,simulation,var,frequency,year,mm,dd,inplace)
                            list_scripts.append(savename)
                else:
                    all_month=pd.date_range(date_init,date_end,freq='M')
                    for ym in all_month:
                            year=ym.year
                            month=ym.month
                            mm="{:02d}".format(month)
                            savename=make_script_archive_1sim_1typ_1month(machine,configuration,simulation,var,frequency,year,mm,inplace)
                            list_scripts.append(savename)

    return list_scripts

def run_all_scripts(list_scripts,machine,configuration,simulations,variables,frequency,date_init,date_end,operation,inplace):
    #Concatenate the name of all simulations and regions
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allvariables=f.concatenate_all_names_in_list(variables)

    #The scripts are run sequentially on the frontal node
    #Get the maximum number of parallel scripts that can run in parallel on one node
    nb_proc_max=20
    #Name of the first mpmd and job file
    mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
    jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
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
                mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                jobname='tmp_job'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
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
    list_scripts=set_up_all_scripts(da.machine,da.configuration,da.simulations,da.variables,da.frequency,da.date_init,da.date_end,da.inplace)
    run_all_scripts(list_scripts,da.machine,da.configuration,da.simulations,da.variables,da.frequency,da.date_init,da.date_end,da.operation,da.inplace)

if __name__ == "__main__":
    main()
