#! /usr/bin/env python

import sys,getopt,os
import argparse
import pandas as pd
import shutil
import subprocess

#Make sure the path to the package is in the PYTHONPATH
from atlas import functions as f
from params import simulations_dict_for_slice as params

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated job")
    parser.add_argument('-param',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check(machine,configuration,simulations,regions,variables,frequency,date_init,date_end):
    #All the checks

    f.check(machine,params.machine_list,'The machine '+str(machine)+' does not exist yet')
    f.check(configuration,params.configuration_list[machine],'The configuration '+str(configuration)+' is not stored on the machine '+str(machine))
       
    for sim in simulations:
        f.check(sim,params.simulation_list[machine][configuration],'The simulation '+str(sim)+' for the configuration '+str(configuration)+' is not stored on the machine '+str(machine))

    for reg in regions:
        f.check(reg,params.regions_list[configuration],'The region '+str(reg)+' is not defined for the configuration '+str(configuration))

    for var in variables:
        f.check(var,params.variable_list,'The variable '+str(var)+' is not defined')

    for sim in simulations:
        for var in variables:
            f.check(frequency,params.frequencies[sim][var],'The variable '+str(var)+' for the simulation '+str(sim)+' does not have the frequency '+str(frequency))

    for sim in simulations:
        if pd.Timestamp(date_init) < pd.Timestamp(params.sim_date_init[sim]):
            sys.exit('The initial date '+str(date_init)+' is not included the period of output of the simulation '+str(sim))
        if pd.Timestamp(date_end) > pd.Timestamp(params.sim_date_end[sim]):
            sys.exit('The end date '+str(date_end)+' is not included the period of output of the simulation '+str(sim))

    print('All checks have passed, we are now going to generate and launch a job that will project '+str(variables)+' from simulations '+str(simulations)+' from configuration '+str(configuration)+' from '+str(date_init)+' to '+str(date_end)+' at '+str(frequency)+' frequency on machine '+str(machine))

def job_operation(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):

    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allregions=f.concatenate_all_names_in_list(regions)
    allvariables=f.concatenate_all_names_in_list(variables)

    all_dates=pd.date_range(date_init,date_end,freq='D')
    for var in variables:
        if params.vars_dim[var]=='2D':
            if operation == 'daily_mean':
                print('We are going to do '+str(operation)+' on variable '+str(var)+' in parallel by month')
                all_month=pd.date_range(date_init,date_end,freq='M')

                # Define the mpmd file name and the job file
                mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
    
                shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

                nb_procs=0
                nb_proc_max=params.mprocs[operation]
                nb_jobs=1

                for ym in all_month:
                    year=ym.year
                    month=ym.month
                    mm="{:02d}".format(month)
                    tag=str(year)+'-'+str(mm)
                    for simulation in simulations:
                        for region in regions:
                            scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                            f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'SCPATH':str(params.scratch_path[machine]),'CDFPATH':str(params.cdf_path[machine]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation])})
                            subprocess.call(["chmod", "+x", scriptname])
                            with open(mpmdname, 'a') as file:
                                file.write("{}\n".format(str(nb_procs)+' ./'+str(scriptname)))

                            nb_procs=nb_procs+1
                            if nb_procs == nb_proc_max:
                                #The job is launched
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
                    subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
                    subprocess.call(["sbatch",jobname])
    
            if operation == 'apply_mask' or operation == 'daily_files':
                print('We are going to do '+str(operation)+' on variable '+str(var)+' in parallel by day')
                all_day=pd.date_range(date_init,date_end,freq='D')

                # Define the mpmd file name and the job file
                mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
    
                shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])


                nb_procs=0
                nb_proc_max=params.mprocs[operation]
                nb_jobs=1

                for d in all_day:
                    year=d.year
                    month=d.month
                    mm="{:02d}".format(month)
                    day=d.day
                    dd="{:02d}".format(day)
                    tag=str(year)+'-'+str(mm)+'-'+str(dd)
                    for simulation in simulations:
                        for region in regions:
                            scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                            if operation == 'apply_mask':
                                f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'MASKNAME':params.mask2Dname[var],'MASKFILE':params.mask[region]})

                            elif operation == 'daily_files':
                                indti,indtf=f.get_ind_xtrac_day_in_month(dd, str(frequency))
                                f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'INDTI':indti,'INDTF':indtf})

                        subprocess.call(["chmod", "+x", scriptname])
                        
                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(str(nb_procs)+' ./'+str(scriptname)))
                                
                        
                        nb_procs=nb_procs+1
                        if nb_procs == nb_proc_max:
                            #The job is launched
                            subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
                            subprocess.call(["sbatch",jobname])
                            
                            #The next job is set up
                            nb_jobs=nb_jobs+1
                            nb_procs=0
                            mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
                            jobname='tmp_job'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'

                            shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                            subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

                if nb_procs > 0:
                    #The last job is launched
                    subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
                    subprocess.call(["sbatch",jobname])

def make_operation(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allregions=f.concatenate_all_names_in_list(regions)
    allvariables=f.concatenate_all_names_in_list(variables)
    mpmdname='tmp_make_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'

    #No job so all will be serial
    all_dates=pd.date_range(date_init,date_end,freq='D')
    for var in variables:
        if params.vars_dim[var]=='2D':
            print('We are going to do '+str(operation)+' on variable '+str(var)+' month by month')
            all_month=pd.date_range(date_init,date_end,freq='M')
            for ym in all_month:
                year=ym.year
                month=ym.month
                mm="{:02d}".format(month)
                tag=str(year)+'-'+str(mm)
                indti,indtf=f.get_ind_xtrac_month_in_year(year, mm, str(frequency))
                for simulation in simulations:
                    for region in regions:
                        scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                        f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'SOSIEPATH':str(params.sosie_path[machine]),'MASKNAME':params.mask2Dname[var],'INDTI':indti,'INDTF':indtf})
                        subprocess.call(["chmod", "+x", scriptname])

                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(' ./'+str(scriptname)))


    print('We are going to run the scripts on the frontal node')
    subprocess.call(["chmod", "+x", mpmdname])
    subprocess.run(params.script_path[machine]+'/'+mpmdname,shell=True)



def main():
    param_dataset = parse_args().param
    da = __import__(param_dataset)

    print('Operation '+str(da.operation)+' for '+str(param_dataset)+' is launched')
    if da.operation == 'apply_mask' or da.operation == 'daily_files' or da.operation == 'daily_mean':
        job_operation(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
    else:
        make_operation(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)



if __name__ == "__main__":
    main()
