#! /usr/bin/env python

import sys,getopt,os, glob
import argparse
import pandas as pd
import shutil
import subprocess
import datetime

#Make sure the path to the package is in the PYTHONPATH
from functions import functions as f
from params import simulations_dict as params
from params import slice_dict as sliced

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated job")
    parser.add_argument('-param',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):
    #All the checks

    f.check(machine,params.machine_list,'The machine '+str(machine)+' does not exist yet')
    f.check(configuration,params.configuration_list[machine],'The configuration '+str(configuration)+' is not stored on the machine '+str(machine))
       
    for simulation in simulations:
        f.check(simulation,params.simulation_list[machine][configuration],'The simulation '+str(simulation)+' for the configuration '+str(configuration)+' is not stored on the machine '+str(machine))

    for region in regions:
        f.check(region,params.regions_list[configuration],'The region '+str(region)+' is not defined for the configuration '+str(configuration))

    for var in variables:
        if var != 'mask':
            f.check(var,params.variable_list,'The variable '+str(var)+' is not defined')

    for simulation in simulations:
        for var in variables:
            if var != 'mask':
                f.check(frequency,params.frequencies[configuration][simulation][var],'The variable '+str(var)+' for the simulation '+str(simulation)+' does not have the frequency '+str(frequency))

    for simulation in simulations:
        if pd.Timestamp(date_init) < pd.Timestamp(params.sim_date_init[configuration][simulation]):
            sys.exit('The initial date '+str(date_init)+' is not included the period of output of the simulation '+str(simulation))
        if pd.Timestamp(date_end) > pd.Timestamp(params.sim_date_end[configuration][simulation]):
            sys.exit('The end date '+str(date_end)+' is not included the period of output of the simulation '+str(simulation))

    print('All checks have passed, we are now going to generate and launch a job or a script that will perform the operation '+str(operation)+' on variables '+str(variables)+' from simulations '+str(simulations)+' from configuration '+str(configuration)+' from '+str(date_init)+' to '+str(date_end)+' at '+str(frequency)+' frequency on machine '+str(machine))


def doc(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation,job,param_dataset):
    #Concatenate the name of all simulations, regions, variables
    allregions=f.concatenate_all_names_in_list(regions)
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allvariables=f.concatenate_all_names_in_list(variables)
    all_dates=pd.date_range(date_init,date_end,freq='D')

    lines = ['The namelist '+param_dataset+' define the following dataset :', 
             'We perform the operation '+operation+' on the variables '+allvariables+' of simulations '+allsimulations+' of the configuration '+configuration,
             'The regions considered are '+allregions+' and the period goes from  '+date_init+' to '+date_end,
             'The operation was done on '+machine+' on '+str(datetime.date.today())]
    with open('readme_'+param_dataset+'.txt', 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

def set_up_script_1simulationu_1region_1var_nomask(machine,configuration,simulation,region,var,frequency,tag,year,mm,operation):
    scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
    if len(tag)==10:
        dd=tag[-2:]

    #Get and fill the right template script depending on the operation
    if operation == 'daily_mean':
        f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'SCPATH':str(sliced.scratch_path[machine]),'CDFPATH':str(sliced.cdf_path[machine]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation])})
    if operation == 'project_sosie':
        indti,indtf=f.get_ind_xtrac_month_in_year(year, mm, str(frequency))
        f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(sliced.scratch_path[machine]),'SOSIEPATH':str(sliced.sosie_path[machine]),'MASKNAME':params.mask2Dname[var],'INDTI':indti,'INDTF':indtf})
    if operation == 'apply_mask':
        f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(sliced.scratch_path[machine]),'MASKNAME':params.mask2Dname[var],'MASKFILE':params.mask[region]})
    if operation == 'daily_files':
        if str(params.frequencies_file[configuration][simulation][var])=='1m':
            indti,indtf=f.get_ind_xtrac_day_in_month(dd, str(frequency))
            f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(sliced.scratch_path[machine]),'INDTI':indti,'INDTF':indtf,'NCOPATH':str(params.nco_path[machine])})
        if str(params.file_frequencies[configuration][simulation][var])=='5d':
            mylist = [files for files in glob.glob(str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_????????-????????.'+str(frequency)+'_'+str(var)+'.nc')]
            file_extract,tag1f,tag2f=f.find_files_containing_1d(mylist,tag)
            indti,indtf=f.get_ind_xtrac_day_in_5days(tag,tag1f,str(frequency))
            f.use_template('script_'+str(operation)+'_2Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'SCPATH':str(sliced.scratch_path[machine]),'INDTI':indti,'INDTF':indtf,'TAG1':tag1f,'TAG2':tag2f,'NCOPATH':str(sliced.nco_path[machine])})
    if operation[:6] == 'degrad':
        if params.vars_dim[var]=='3D':
            f.use_template('script_'+str(operation[:6])+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[configuration][simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'RATIO':str(operation[6:]),'VARTYP':str(params.varpt[var]), 'SCPATH':str(sliced.scratch_path[machine]),'CDFPATH':str(sliced.cdf_path[machine]),'MASKFILE':str(params.maskfile[machine][configuration][region]),'MESHHFILE':str(params.mesh_hgr[machine][configuration][region]),'MESHZFILE':str(params.mesh_zgr[machine][configuration][region])})
        if params.vars_dim[var]=='2D':
            f.use_template('script_'+str(operation[:6])+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'RATIO':str(operation[6:]),'VARTYP':str(params.varpt[var]), 'SCPATH':str(sliced.scratch_path[machine]),'CDFPATH':str(sliced.cdf_path[machine]),'MASKFILE':str(params.maskfile[machine][configuration][region]),'MESHHFILE':str(params.mesh_hgr[machine][configuration][region]),'MESHZFILE':str(params.mesh_zgr[machine][configuration][region])})
    if operation == 'extract':
        if params.vars_dim[var]=='3D':
            outputname=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'d'+str(dd)+'.'+str(frequency)+'_'+str(var)+'.nc'
        if params.vars_dim[var]=='2D':
            outputname=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'d01.'+str(frequency)+'_'+str(var)+'.nc'
        if not os.path.exists(outputname):
           if params.vars_dim[var]=='3D':
               f.use_template('script_'+str(operation)+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[configuration][simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'FILETYP':str(params.filetyp[configuration][simulation][var]), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'XX1':str(params.xy[configuration][region][0]),'XX2':str(params.xy[configuration][region][1]),'YY1':str(params.xy[configuration][region][2]),'YY2':str(params.xy[configuration][region][3]),'SCPATH':str(sliced.scratch_path[machine]),'NCOPATH':str(sliced.nco_path[machine])})
           if params.vars_dim[var]=='2D':
               f.use_template('script_'+str(operation)+'_2Dvar_1month_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[configuration][simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm), 'FILETYP':str(params.filetyp[configuration][simulation][var]), 'SOURCEDIR':str(params.directory[machine][configuration][simulation]), 'STYLENOM':str(params.stylenom[machine][configuration][simulation]),'XX1':str(params.xy[configuration][region][0]),'XX2':str(params.xy[configuration][region][1]),'YY1':str(params.xy[configuration][region][2]),'YY2':str(params.xy[configuration][region][3]),'SCPATH':str(sliced.scratch_path[machine]),'NCOPATH':str(sliced.nco_path[machine])})

        else:
            return None
    if operation == 'compute_buoyancy':
        outputname=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'-S/'+str(frequency)+'/'+str(region)+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'d'+str(dd)+'.'+str(frequency)+'_buoyancy.nc'
        if not os.path.exists(outputname):
            f.use_template('script_'+str(operation)+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[configuration][simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'SCPATH':str(sliced.scratch_path[machine]),'CDFPATH':str(sliced.cdf_path[machine]),'MASKFILE':str(params.maskfile[machine][configuration][region]),'MESHHFILE':str(params.mesh_hgr[machine][configuration][region]),'MESHZFILE':str(params.mesh_zgr[machine][configuration][region])})
        else:
            return None
    if operation == 'compute_curl':
        outputname=str(sliced.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'-S/'+str(frequency)+'/'+str(region)+'/'+str(configuration)+str(sliced.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'d'+str(dd)+'.'+str(frequency)+'_curl.nc'
        if not os.path.exists(outputname):
            f.use_template('script_'+str(operation)+'_3Dvar_1day_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(sliced.ex[configuration][region]), 'REGIONNAME':str(region),'VARIABLE':str(var), 'VNAME':str(params.vars_name[configuration][simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'DAY':str(dd),'SCPATH':str(sliced.scratch_path[machine]),'CDFPATH':str(sliced.cdf_path[machine]),'MASKFILE':str(params.maskfile[machine][configuration][region]),'MESHHFILE':str(params.mesh_hgr[machine][configuration][region]),'MESHZFILE':str(params.mesh_zgr[machine][configuration][region])})
        else:
            return None

    #Add the script to the mpmpd conf file
    subprocess.call(["chmod", "+x", scriptname])
    return scriptname

def set_up_script_1simulation_1region_mask(machine,configuration,simulation,region,var,frequency,date_init,date_end,operation):
    scriptname=('tmp_script_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(region)+'_mask.ksh')
    if operation == 'extract':
        f.use_template('script_'+str(operation)+'_mesh_mask_files_template.ksh', scriptname, {'CONFIGURATION':str(configuration),'REGIONNAME':str(region),'REGIONABR':str(sliced.ex[configuration][region]),'MESHHFILE':str(params.mesh_hgr[machine][configuration][configuration]),'MESHZFILE':str(params.mesh_zgr[machine][configuration][configuration]),'MASKFILE':str(params.maskfile[machine][configuration][configuration]),'BATHYFILE':str(params.bathyfile[machine][configuration][configuration]),'XX1':str(params.xy[configuration][region][0]),'XX2':str(params.xy[configuration][region][1]),'YY1':str(params.xy[configuration][region][2]),'YY2':str(params.xy[configuration][region][3]),'SCPATH':str(sliced.scratch_path[machine]),'NCOPATH':str(sliced.nco_path[machine])})
    #Add the script to the mpmpd conf file
    subprocess.call(["chmod", "+x", scriptname])
    return scriptname


def set_up_all_scripts(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):

    list_scripts=[]
    
    #Loop over the variables
    for var in variables:

        #Operations on mask do not deal with time
        if var == 'mask':
            #no dates, loop over simulations and regions
            for simulation in simulations:
                for region in regions:
                    scriptname=set_up_script_1simulation_1region_mask(machine,configuration,simulation,region,var,frequency,date_init,date_end,operation)
                    list_scripts.append(scriptname)

        else:
            #For variable other than mask, determine the frequency of parallelization
            if params.vars_dim[var]=='2D':
                if operation == 'daily_mean' or operation == 'project_sosie' or operation[:6] == 'degrad' or operation == 'extract':
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
                        scriptname=set_up_script_1simulationu_1region_1var_nomask(machine,configuration,simulation,region,var,frequency,tag,year,mm,operation)
                        if scriptname is not None:
                            list_scripts.append(scriptname)
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


    print('Check if simulations details are all defined')
    check(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
    #print('Check if operation is permitted and document the process')
    #doc(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation,da.job,param_dataset)
    print('Set up scripts and running them for operation '+str(da.operation)+' for '+str(param_dataset))
    list_scripts=set_up_all_scripts(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
    run_all_scripts(list_scripts,da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation,da.job)


if __name__ == "__main__":
    main()
