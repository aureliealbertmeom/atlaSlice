#! /usr/bin/env python

import sys,getopt,os,glob
import argparse
import pandas as pd
import subprocess
import shutil

#Make sure the path to the package is in the PYTHONPATH
from atlas import functions as f
from params import simulations_dict_for_slice as params

def parse_args():
    parser=argparse.ArgumentParser(description="save the requested extractions defined in dataset in a compact form on the store filesystem")
    parser.add_argument('-param',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def save(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,inplace):
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allregions=f.concatenate_all_names_in_list(regions)
    allvariables=f.concatenate_all_names_in_list(variables)
    mpmdname='tmp_make_save_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'

    for simulation in simulations:
        for region in regions:
            for var in variables:

                if params.vars_dim[var]=='2D':
                    all_month=pd.date_range(date_init,date_end,freq='M')
                    if len(all_month) < 13:
                        yeari=all_month[0].year
                        yearf=all_month[-1].year
                        if yeari == yearf:
                            year=yeari
                            tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'.'+str(frequency)+'_'+str(var)+'.tar'
                            savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(year)+'.ksh'
                            f.use_template('script_save_2Dvar_1year_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'TARNAME':str(tarname), 'SCPATH':str(params.scratch_path[machine]), 'STPATH':str(params.store_path[machine]),'YON':inplace})
                            subprocess.call(["chmod", "+x", savename])

                            with open(mpmdname, 'a') as file:
                                file.write("{}\n".format(' ./'+str(savename)))
                        else:
                            for year in [yeari,yearf]:
                                tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'.'+str(frequency)+'_'+str(var)+'.tar'
                                savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(year)+'.ksh'
                                f.use_template('script_save_2Dvar_1year_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'TARNAME':str(tarname), 'SCPATH':str(params.scratch_path[machine]), 'STPATH':str(params.store_path[machine]),'YON':inplace})
                                subprocess.call(["chmod", "+x", savename])

                                with open(mpmdname, 'a') as file:
                                    file.write("{}\n".format(' ./'+str(savename)))

                elif params.vars_dim[var]=='3D':
                    all_month=pd.date_range(date_init,date_end,freq='M')
                    if len(all_month) < 13:
                        yeari=all_month[0].year
                        yearf=all_month[-1].year
                        if yeari == yearf:
                            year=yeari
                            for date in all_month:
                                month="{:02d}".format(date.month)
                                tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(month)+'.'+str(frequency)+'_'+str(var)+'.tar'
                                savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(year)+'m'+str(month)+'.ksh'
                                f.use_template('script_save_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(params.vars_name[simulation][var]),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(month), 'TARNAME':str(tarname), 'SCPATH':str(params.scratch_path[machine]), 'STPATH':str(params.store_path[machine]),'YON':inplace})
                                subprocess.call(["chmod", "+x", savename])

                                with open(mpmdname, 'a') as file:
                                    file.write("{}\n".format(' ./'+str(savename)))
                        else:
                            for year in [yeari,yearf]:
                                for date in all_month:
                                    month="{:02d}".format(date.month)
                                    tarname=str(configuration)+str(params.ex[configuration][region])+'-'+str(simulation)+'_y'+str(year)+'m'+str(month)+'.'+str(frequency)+'_'+str(var)+'.tar'
                                    savename='tmp_script_save_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(year)+'m'+str(month)+'.ksh'
                                    f.use_template('script_save_3Dvar_1month_template.ksh', savename, {'CONFIGURATION':str(configuration),'SIMULATION':str(simulation),'REGIONABR':str(params.ex[configuration][region]), 'REGIONNAME':str(region), 'VARIABLE':str(var),'FREQUENCY':str(frequency), 'YEAR':str(year), 'MONTH':str(month), 'TARNAME':str(tarname), 'SCPATH':str(params.scratch_path[machine]), 'STPATH':str(params.store_path[machine]),'YON':inplace})
                                    subprocess.call(["chmod", "+x", savename])

                                    with open(mpmdname, 'a') as file:
                                        file.write("{}\n".format(' ./'+str(savename)))




    print('We are going to run the save scripts on the frontal node')
    subprocess.call(["chmod", "+x", mpmdname])
    subprocess.run(params.script_path[machine]+'/'+mpmdname,shell=True)

def main():
    param_dataset = parse_args().param
    da = __import__(param_dataset)

    print('Extractions for '+str(param_dataset)+' are saved')
    save(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.inplace)
        
    if da.operation == '1d-mean':
        save(da.machine,da.configuration,da.simulations,da.regions,da.variables,'1d',da.date_init,da.date_end,da.inplace)
if __name__ == "__main__":
    main()

