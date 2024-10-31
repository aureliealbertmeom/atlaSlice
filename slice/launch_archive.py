#! /usr/bin/env python

import sys,getopt,os,glob
import argparse
import pandas as pd
import shutil
import subprocess
import numpy as np

#Make sure the path to the package is in the PYTHONPATH
from functions import functions as f
from params import simulations_dict_for_slice as params

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated job")
    parser.add_argument('-param',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check_output(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):

    #Check wether the desired outputs have been produced
    for simulation in simulations:
        for region in regions:
            nb_month=0
            nb_day=0
            for var in variables:
                if params.file_frequencies[simulation][var]=='1d':
                    all_day=pd.date_range(date_init,date_end,freq='D')
                    nb_day=nb_day+len(all_day)
                if params.file_frequencies[simulation][var]=='1m':
                    all_month=pd.date_range(date_init,date_end,freq='M')
                    nb_month=nb_month+len(all_month)
            nb_files_expected=nb_month+nb_day

            #Depending on the operation the outputs are poduced in different directories
            match operation:
                case 'extract':
                    tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
            if operation[:6] == 'degrad':
                tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'-'+str(operation)+'/'+str(frequency)

            #Counting the files in the directory
            files_list = glob.glob(tdir+'/'+str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_*.'+str(frequency)+'_*.nc')
            nb_files_obtained=len(files_list)
            print(str(nb_files_obtained)+' out of '+str(nb_files_expected)+' files were produced for the operation '+str(operation)+' on simulation '+str(simulation)+' and region '+str(region)+' in '+str(tdir))

            if nb_files_obtained != nb_files_expected:
                for var in variables:
                    if params.file_frequencies[simulation][var]=='1d':
                        all_day=pd.date_range(date_init,date_end,freq='D')
                        nb_files_expected=len(all_day)
                        nb_day=nb_day+len(all_day)
                        nb_files_obtained=len([name for name in glob.glob(tdir+'/*'+str(var)+'*') if os.path.isfile(name)])
                        print(str(nb_files_obtained)+' out of '+str(nb_files_expected)+' files were extracted for '+str(var)+' from simulation '+str(simulation)+' and region '+str(region)+' in '+str(tdir))
                    if params.file_frequencies[simulation][var]=='1m':
                        all_month=pd.date_range(date_init,date_end,freq='M')
                        nb_files_expected=len(all_month)
                        nb_files_obtained=len([name for name in glob.glob(tdir+'/*'+str(var)+'*') if os.path.isfile(name)])
                        print(str(nb_files_obtained)+' out of '+str(nb_files_expected)+' files were extracted for '+str(var)+' from simulation '+str(simulation)+' and region '+str(region)+' in '+str(tdir))



def make_archive(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allregions=f.concatenate_all_names_in_list(regions)
    allvariables=f.concatenate_all_names_in_list(variables)
    mpmdname='tmp_make_'+str(operation)+'_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'

    for simulation in simulations:
        for region in regions:
            for var in variables:
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
                            tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
                            tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'.'+str(frequency)+'_'+str(var)+'-'+str(operation)+'.tar'
                            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(year)+'.ksh'
                            f.use_template('script_save_2Dvar_1year_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})
                        if operation[:6] == 'degrad':
                            tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'-'+str(operation)+'/'+str(frequency)
                            tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'.'+str(frequency)+'_'+str(var)+'-'+str(operation)+'.tar'
                            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'-'+str(operation)+'_'+str(frequency)+'_'+str(year)+'.ksh'
                            f.use_template('script_save_2Dvar_1year_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var)+'-'+str(operation),'FREQUENCY':str(frequency), 'YEAR':str(year), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})
 
                        subprocess.call(["chmod", "+x", savename])

                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(' ./'+str(savename)))

                if freq_par == '1m':
                    all_month=pd.date_range(date_init,date_end,freq='M')
                    for ym in all_month:
                        year=ym.year
                        month=ym.month
                        mm="{:02d}".format(month)
                        if operation == 'extract':
                            tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
                            tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'.'+str(frequency)+'_'+str(var)+'.tar'
                            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'-'+str(operation)+'_'+str(frequency)+'_'+str(year)+str(mm)+'.ksh'
                            f.use_template('script_save_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year),'MONTH':str(mm), 'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})
                        if operation[:6] == 'degrad':
                            tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'-'+str(operation)+'/'+str(frequency)
                            tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(mm)+'.'+str(frequency)+'_'+str(var)+'-'+str(operation)+'.tar'
                            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'-'+str(operation)+'_'+str(frequency)+'_'+str(year)+str(mm)+'.ksh'
                            f.use_template('script_save_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var)+'-'+str(operation),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(mm),'TARNAME':str(tarname), 'SCPATH':str(tdir), 'STPATH':str(params.store_path[machine])})
 
                        subprocess.call(["chmod", "+x", savename])

                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(' ./'+str(savename)))

    print('We are going to run the scripts on the frontal node')
    subprocess.call(["chmod", "+x", mpmdname])
    subprocess.run(params.script_path[machine]+'/'+mpmdname,shell=True)



def main():
    param_dataset = parse_args().param
    da = __import__(param_dataset)

    print('Checking the number of files produced for operation '+str(da.operation)+' for '+str(param_dataset))
    check_output(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)
    if da.archive == 'Y':
        print('Archive for operation '+str(da.operation)+' for '+str(param_dataset)+' is launched')
        make_archive(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)


if __name__ == "__main__":
    main()
