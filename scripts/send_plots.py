#! /usr/bin/env python

import sys,getopt,os
from pathlib import Path
import argparse
import pandas as pd
import shutil
import subprocess
#Make sure the path to the package is in the PYTHONPATH
from atlas import plots as pl
from atlas import functions as f
from params import simulations_dict as params

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated make")
    parser.add_argument('-dataset',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check(machine,configuration,simulations,variables,plot_regions,frequency,date_init,date_end):
    #All the checks

    f.check(machine,params.machine_list,'The machine '+str(machine)+' does not exist yet')
    f.check(configuration,params.configuration_list[machine],'The configuration '+str(configuration)+' is not stored on the machine '+str(machine))
       
    for sim in simulations:
        f.check(sim,params.simulation_list[machine][configuration],'The simulation '+str(sim)+' for the configuration '+str(configuration)+' is not stored on the machine '+str(machine))

    for var in variables:
        f.check(var,params.variable_list,'The variable '+str(var)+' is not defined')

    for preg in plot_regions:
        f.check(preg,params.regions_list[configuration],'The region '+str(preg)+' is not defined for the configuration '+configuration)

    for sim in simulations:
        for var in variables:
            f.check(frequency,params.frequencies[sim][var],'The variable '+str(var)+' for the simulation '+str(sim)+' does not have the frequency '+str(frequency))

    for sim in simulations:
        if pd.Timestamp(date_init) < pd.Timestamp(params.sim_date_init[sim]):
            sys.exit('The initial date '+str(date_init)+' is not included the period of output of the simulation '+str(sim))
        if pd.Timestamp(date_end) > pd.Timestamp(params.sim_date_end[sim]):
            sys.exit('The end date '+str(date_end)+' is not included the period of output of the simulation '+str(sim))

    print('All checks have passed, we are now going to generate and launch a make that will plot '+str(variables)+' from simulations '+str(simulations)+' from configuration '+str(configuration)+' from '+str(date_init)+' to '+str(date_end)+' at '+str(frequency)+' frequency on machine '+str(machine))


def send_plot(machine,configuration,simulations,variables,plot_type,plot_locs,plot_regions,frequency,date_init,date_end,ttime):
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allvariables=f.concatenate_all_names_in_list(variables)
    allregions=f.concatenate_all_names_in_list(plot_regions)
    alllocs=f.concatenate_all_names_in_list(plot_locs)
    tag=f.tag_from_string_date(date_end,params.stylenom[machine][configuration][simulations[0]])
    mpmdname='tmp_send_plot_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(allregions)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
    

    #Loop over all the simulations, variables, type, region and locations of the plots requested
    for sim in simulations:
            for var in variables:
                for loc in plot_locs:
                    for reg in plot_regions:
                        if plot_type == 'map_noproj' or plot_type == 'map':
                            scriptname='tmp_script_send_'+str(machine)+'_'+str(configuration)+'_'+str(sim)+'_'+str(var)+'_'+str(reg)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
                        if plot_type == 'section':
                            scriptname='tmp_script_send_'+str(machine)+'_'+str(configuration)+'_'+str(sim)+'_'+str(var)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(frequency)+'_'+str(tag)+'.ksh'
                        plotname=str(configuration)+'-'+str(sim)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(reg)+'_'+str(tag)+'.'+str(frequency)+'_'+str(var)+'_t'+str(ttime)+'.png'
                            
                        plotdir=params.scratch_path[machine]+'/'+str(configuration)+'/'+str(configuration)+'-'+str(sim)
                        shutil.copyfile('script_send_'+str(machine)+'.ksh',scriptname)
                        subprocess.call(["sed", "-i", "-e",  's/CONFIGURATION/'+str(configuration)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/SIMULATION/'+str(sim)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/PLOTNAME/'+str(plotname)+'/g', scriptname])
                        if plot_type == 'map_noproj' or plot_type == 'map':
                            subprocess.call(["sed", "-i", "-e",  's/REGION/'+str(reg)+'/g', scriptname])
                        if plot_type == 'section':
                            subprocess.call(["sed", "-i", "-e",  's/REGION/SECTIONS/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%PLOTDIR%'+str(plotdir)+'%g', scriptname])
                        subprocess.call(["chmod", "+x", scriptname])
                            
                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(' ./'+str(scriptname)))
                            


    #Copy the template make for the given machine and name the make according to the specs
    subprocess.call(["chmod", "+x", mpmdname])
    subprocess.run(params.script_path[machine]+'/scripts/'+mpmdname,shell=True)


def main():
    #Import the plots definition, the script name is the argument dataset
    param_dataset = parse_args().dataset
    da = __import__(param_dataset)
    

    for ttime in da.plots_to_be_sent:
        send_plot(da.machine,da.configuration,da.simulations,da.variables,da.plot_type,da.plot_locs,da.plot_regions,da.frequency,da.date_init,da.date_end,ttime)


if __name__ == "__main__":
    main()

