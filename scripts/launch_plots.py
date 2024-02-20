#! /usr/bin/env python

import sys,getopt,os
from pathlib import Path
import argparse
import pandas as pd
import shutil
import subprocess
import math as ma
import numpy as np

#Make sure the path to the package is in the PYTHONPATH
from atlas import plots as pl
from atlas import functions as f
from params import simulations_dict as params

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated job")
    parser.add_argument('-dataset',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check(machine,config,simulations,variables,plot_type,plot_locs,plot_regions,frequency,date_init,date_end):
    #All the checks

    f.check(machine,params.machine_list,'The machine '+str(machine)+' does not exist yet')
    f.check(config,params.configuration_list[machine],'The config '+str(config)+' is not stored on the machine '+str(machine))
       
    for sim in simulations:
        f.check(sim,params.simulation_list[machine][config],'The simulation '+str(sim)+' for the config '+str(config)+' is not stored on the machine '+str(machine))

    for var in variables:
        f.check(var,params.variable_list,'The variable '+str(var)+' is not defined')

    match plot_type:
        case 'map_noproj':
            for preg in plot_regions:
                f.check(preg,params.regions_list[config],'The region '+str(preg)+' is not defined for the config '+config)
        case 'section':
            for sloc in plot_locs:
                f.check(sloc,params.sections_list[config],'The section '+str(sloc)+' is not defined for the config '+config)

    for sim in simulations:
        for var in variables:
            f.check(frequency,params.frequencies[sim][var],'The variable '+str(var)+' for the simulation '+str(sim)+' does not have the frequency '+str(frequency))

    for sim in simulations:
        if pd.Timestamp(date_init) < pd.Timestamp(params.sim_date_init[sim]):
            sys.exit('The initial date '+str(date_init)+' is not included the period of output of the simulation '+str(sim))
        if pd.Timestamp(date_end) > pd.Timestamp(params.sim_date_end[sim]):
            sys.exit('The end date '+str(date_end)+' is not included the period of output of the simulation '+str(sim))

    print('All checks have passed, we are now going to generate and launch a job that will plot '+str(variables)+' from simulations '+str(simulations)+' from config '+str(config)+' from '+str(date_init)+' to '+str(date_end)+' at '+str(frequency)+' frequency on machine '+str(machine))

def job(machine,config,simulations,variables,plot_type,plot_locs,plot_regions,frequency,date_init,date_end):


    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allvariables=f.concatenate_all_names_in_list(variables)
    alllocs=f.concatenate_all_names_in_list(plot_locs)


    # Define the mpmd file name and the job file
    if plot_type == 'map_noproj' and plot_locs[0] == 'surf' and params.vars_dim[variables[0]] == '2D':
        allregions=f.concatenate_all_names_in_list(plot_regions)
        mpmdname='tmp_mpmd_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(allregions)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(f.tag_from_string_date(date_init,params.stylenom[machine][config][simulations[0]]))+'-'+str(f.tag_from_string_date(date_end,params.stylenom[machine][config][simulations[0]]))+'.conf'
        jobname='tmp_job_plot_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(allregions)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(f.tag_from_string_date(date_init,params.stylenom[machine][config][simulations[0]]))+'-'+str(f.tag_from_string_date(date_end,params.stylenom[machine][config][simulations[0]]))+'.ksh'
    elif plot_type == 'section' and params.vars_dim[variables[0]] == '3D':
        mpmdname='tmp_mpmd_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(f.tag_from_string_date(date_init,params.stylenom[machine][config][simulations[0]]))+'-'+str(f.tag_from_string_date(date_end,params.stylenom[machine][config][simulations[0]]))+'.conf'
        jobname='tmp_job_plot_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(f.tag_from_string_date(date_init,params.stylenom[machine][config][simulations[0]]))+'-'+str(f.tag_from_string_date(date_end,params.stylenom[machine][config][simulations[0]]))+'.ksh'

    shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
    subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])
    #Loop over all the simulations, variables, type, region and locations of the plots requested
    nb_procs=0
    nb_proc_max=params.mprocs[plot_type]
    nb_jobs=1
    
    #We assume all variables have the same output frequency for every simulations requested 
    freq_file=params.frequencies_file[simulations[0]][variables[0]]
    all_dates=pd.date_range(date_init,date_end,freq=freq_file)

    #Loop over the output files
    for date in all_dates:
        # Create a time tag from the date
        tag=f.tag_from_string_date(date,params.stylenom[machine][config][simulations[0]])
        for sim in simulations:
            for var in variables:
                for loc in plot_locs:
                    for reg in plot_regions:
                        if plot_type == 'map_noproj' and loc == 'surf' and params.vars_dim[var] == '2D':
                            scriptname='tmp_script_plot_'+str(machine)+'_'+str(config)+'_'+str(sim)+'_'+str(var)+'_'+str(reg)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
                        elif plot_type == 'section' and params.vars_dim[var] == '3D':
                            scriptname='tmp_script_plot_'+str(machine)+'_'+str(config)+'_'+str(sim)+'_'+str(var)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
                        shutil.copyfile('script_plot_'+str(machine)+'.ksh',scriptname)
                        subprocess.call(["sed", "-i", "-e",  's/MACHINE/'+str(machine)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/CONFIGURATION/'+str(config)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/SIMULATION/'+str(sim)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/VARIABLE/'+str(var)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/PLOTREGION/'+str(reg)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/TYPE/'+str(plot_type)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/LOCATION/'+str(loc)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/FREQUENCY/'+str(frequency)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/DATE/'+str(date)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%SCRIPTDIR%'+str(params.script_path[machine])+'%g', scriptname])
                        subprocess.call(["chmod", "+x", scriptname])
                            
                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(str(nb_procs)+' ./'+str(scriptname)))
                                
                        nb_procs=nb_procs+1
                        if nb_procs == nb_proc_max:
                            #The job is launched
                            subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
#                            subprocess.call(["sbatch",jobname])
        
                            #The next job is set up
                            nb_jobs=nb_jobs+1
                            nb_procs=0
                            if plot_type == 'map_noproj' and loc == 'surf' and params.vars_dim[var] == '2D':
                                jobname='tmp_job'+str(nb_jobs)+'_plot_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(allregions)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
                                mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(allregions)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(tag)+'.conf'
                            elif plot_type == 'section' and params.vars_dim[variables[0]] == '3D':
                                jobname='tmp_job'+str(nb_jobs)+'_plot_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
                                mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(machine)+'_'+str(config)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(tag)+'.conf'
                                
                            shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                            subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

        if nb_procs > 0:
            #The last job is launched
            subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
            subprocess.call(["sbatch",jobname])


def main():
    #Import the plots definition, the script name is the argument dataset
    param_dataset = parse_args().dataset
    da = __import__(param_dataset)
    
    check(da.machine,da.configuration,da.simulations,da.variables,da.plot_type,da.plot_locs,da.plot_regions,da.frequency,da.date_init,da.date_end)
    job(da.machine,da.configuration,da.simulations,da.variables,da.plot_type,da.plot_locs,da.plot_regions,da.frequency,da.date_init,da.date_end)


if __name__ == "__main__":
    main()

