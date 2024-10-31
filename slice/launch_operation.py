#! /usr/bin/env python

import sys,getopt,os, glob
import argparse
import pandas as pd
import shutil
import subprocess

#Make sure the path to the package is in the PYTHONPATH
from functions import functions as f
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
    allregions=f.concatenate_all_names_in_list(regions)

    #Loop over the variables
    for var in variables:

        if var == 'mask':
            # Define the mpmd file name and the job file, no dates, frequency or simulation associated with mask
            mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allregions)+'_'+str(var)+'.ksh'
            jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
        else:
            allsimulations=f.concatenate_all_names_in_list(simulations)
            allvariables=f.concatenate_all_names_in_list(variables)
            all_dates=pd.date_range(date_init,date_end,freq='D')
            # Define the mpmd file name and the job file
            mpmdname='tmp_mpmd_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
            jobname='tmp_job_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(var)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
        
        shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
        subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

        nb_procs=0
        if operation[:6] == 'degrad':
            nb_proc_max=params.mprocs[operation[:6]]
        else:
            nb_proc_max=params.mprocs[operation]
        nb_jobs=1

        #Determine the frequency of parallelization
        if var == 'mask':
            #no dates, loop over regions
            for region in regions:
                scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(region)+'.ksh')
                if operation == 'extract':
                    f.use_template('script_'+str(operation)+'_mesh_mask_files_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'REGIONABR':str(params.ex[configuration][region]),'MESHHFILE':str(params.mesh_hgr[configuration][configuration]),'MESHZFILE':str(params.mesh_zgr[configuration][configuration]),'MASKFILE':str(params.mask[configuration][configuration]),'XTRACTINDICES':str(params.xy[configuration][region]),'SCPATH':str(params.scratch_path[machine]),'NCOPATH':str(params.nco_path[machine])})
                    #Add the script to the mpmpd conf file
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
                        mpmdname='tmp_mpmd'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allregions)+'.ksh'
                        jobname='tmp_job'+str(nb_jobs)+'_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allregions)+'.ksh'
                        shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
                        subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])

            if nb_procs > 0:
                #The last job is launched
                subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
                subprocess.call(["sbatch",jobname])
            exit()



        if params.vars_dim[var]=='2D':
            if operation == 'daily_mean' or operation == 'project_sosie' or operation[:6] == 'degrad':
                freq_par='1m'
                print('We are going to do '+str(operation)+' on variable '+str(var)+' in parallel by month')
                incr_temp=pd.date_range(date_init,date_end,freq='M')
            if operation == 'apply_mask' or operation == 'daily_files':
                freq_par='1d'
                print('We are going to do '+str(operation)+' on variable '+str(var)+' in parallel by day')
                incr_temp=pd.date_range(date_init,date_end,freq='D')
        if params.vars_dim[var]=='3D':
            if operation[:6] == 'degrad' or 'extract':
                freq_par='1d'
                if operation[:6] == 'degrad':
                    print('We are going to degrad variable '+str(var)+' with a ratio of '+str(operation[6:])+' in parallel by day')
                if operation[:6] == 'extract':
                    print('We are going to extract variable '+str(var)+' in parallel by day')
                incr_temp=pd.date_range(date_init,date_end,freq='D')

        #Loop over the dates composing the period
        for ym in incr_temp:
            year=ym.year
            month=ym.month
            mm="{:02d}".format(month)
            if freq_par == '1m':
                tag=str(year)+'-'+str(mm)
            if freq_par == '1d':
                day=ym.day
                dd="{:02d}".format(day)
                tag=str(year)+'-'+str(mm)+'-'+str(dd)

            #Loop over simulations and regions
            for simulation in simulations:
                for region in regions:
                    scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')

                    #Get and fill the right template script depending on the operation
                    if operation == 'daily_mean':
                        f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'SCPATH':str(params.scratch_path[machine]),'CDFPATH':str(params.cdf_path[machine]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation])})
                    if operation == 'project_sosie':
                        indti,indtf=f.get_ind_xtrac_month_in_year(year, mm, str(frequency))
                        f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'SOSIEPATH':str(params.sosie_path[machine]),'MASKNAME':params.mask2Dname[var],'INDTI':indti,'INDTF':indtf})
                    if operation == 'apply_mask':
                        f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'MASKNAME':params.mask2Dname[var],'MASKFILE':params.mask[region]})
                    if operation == 'daily_files':
                        if str(params.file_frequencies[simulation][var])=='1m':
                            indti,indtf=f.get_ind_xtrac_day_in_month(dd, str(frequency))
                            f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'INDTI':indti,'INDTF':indtf,'NCOPATH':str(params.nco_path[machine])})
                        if str(params.file_frequencies[simulation][var])=='5d':
                            mylist = [files for files in glob.glob(str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)+'/'+str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_????????-????????.'+str(frequency)+'_'+str(var)+'.nc')]
                            file_extract,tag1f,tag2f=f.find_files_containing_1d(mylist,tag)
                            indti,indtf=f.get_ind_xtrac_day_in_5days(tag,tag1f,str(frequency))
                            f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'INDTI':indti,'INDTF':indtf,'TAG1':tag1f,'TAG2':tag2f,'NCOPATH':str(params.nco_path[machine])})
                    if operation[:6] == 'degrad':
                        if params.vars_dim[var]=='3D':
                            f.use_template('script_'+str(operation[:6])+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'RATIO':str(operation[6:]),'VARTYP':str(params.varpt[var]), 'SCPATH':str(params.scratch_path[machine]),'CDFPATH':str(params.cdf_path[machine]),'MASKFILE':str(params.mask[configuration][region]),'MESHHFILE':str(params.mesh_hgr[configuration][region]),'MESHZFILE':str(params.mesh_zgr[configuration][region])})
                        if params.vars_dim[var]=='2D':
                            f.use_template('script_'+str(operation[:6])+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'RATIO':str(operation[6:]),'VARTYP':str(params.varpt[var]), 'SCPATH':str(params.scratch_path[machine]),'CDFPATH':str(params.cdf_path[machine]),'MASKFILE':str(params.mask[configuration][region]),'MESHHFILE':str(params.mesh_hgr[configuration][region]),'MESHZFILE':str(params.mesh_zgr[configuration][region])})
                    if operation == 'extract':
                        f.use_template('script_'+str(operation)+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'FILETYP':str(params.filetyp[simulation][var]), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'XTRACTINDICES':str(params.xy[configuration][region]),'SCPATH':str(params.scratch_path[machine]),'NCOPATH':str(params.nco_path[machine])})

                    #Add the script to the mpmpd conf file
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
            if len(all_month)==0:
                sys.exit("Not enough months to perform the operation by month")
            for ym in all_month:
                year=ym.year
                month=ym.month
                mm="{:02d}".format(month)
                tag=str(year)+'-'+str(mm)
                for simulation in simulations:
                    for region in regions:
                        scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                        if operation == 'extract':
                            f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'FILETYP':str(params.filetyp[simulation][var]), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'XTRACTINDICES':str(params.xy[configuration][region]),'SCPATH':str(params.scratch_path[machine]),'NCOPATH':str(params.nco_path[machine])})

                        if operation == 'project_sosie':
                            indti,indtf=f.get_ind_xtrac_month_in_year(year, mm, str(frequency))
                            f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(params.scratch_path[machine]),'SOSIEPATH':str(params.sosie_path[machine]),'MASKNAME':params.mask2Dname[var],'INDTI':indti,'INDTF':indtf})
                        subprocess.call(["chmod", "+x", scriptname])

                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(' ./'+str(scriptname)))

        if params.vars_dim[var]=='3D':
            print('We are going to do '+str(operation)+' on variable '+str(var)+' day by day')
            all_day=pd.date_range(date_init,date_end,freq='D')
            for dm in all_day:
                year=dm.year
                month=dm.month
                mm="{:02d}".format(month)
                day=dm.day
                dd="{:02d}".format(day)
                tag=str(year)+'-'+str(mm)+'-'+str(dd)
                for simulation in simulations:
                    for region in regions:
                        scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                        if operation == 'extract':
                            f.use_template('script_'+str(operation)+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'FILETYP':str(params.filetyp[simulation][var]), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'XTRACTINDICES':str(params.xy[configuration][region]),'SCPATH':str(params.scratch_path[machine]),'NCOPATH':str(params.nco_path[machine])})
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
    match da.job:
        case 'Y':
            job_operation(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
        case 'N':
            make_operation(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)


if __name__ == "__main__":
    main()
