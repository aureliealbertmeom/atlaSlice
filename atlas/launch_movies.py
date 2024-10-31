#! /usr/bin/env python

import sys,getopt,os
from pathlib import Path
import argparse
import pandas as pd
import shutil
import subprocess
#Make sure the path to the package is in the PYTHONPATH
from functions import plots as pl
from functions import functions as f
from params import simulations_dict as params

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated make")
    parser.add_argument('-dataset',type=str,help='dataset param')
    args=parser.parse_args()
    return args


def make_movies(machine,configuration,simulations,variables,plot_type,plot_locs,plot_regions,frequency,date_init,date_end):
    #We assume all variables have the same output frequency for every simulations requested
    freq_file=params.frequencies_file[simulations[0]][variables[0]]
        
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allvariables=f.concatenate_all_names_in_list(variables)
    allregions=f.concatenate_all_names_in_list(plot_regions)
    alllocs=f.concatenate_all_names_in_list(plot_locs)
    mpmdname='tmp_make_movies_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allvariables)+'_'+str(allregions)+'_'+str(plot_type)+'_'+str(alllocs)+'_'+str(frequency)+'.ksh'
    

    #Loop over all the simulations, variables, type, region and locations of the plots requested
    for sim in simulations:
                for var in variables:
                    for reg in plot_regions:
                            for loc in plot_locs:
                                scriptname='tmp_script_movie_'+str(machine)+'_'+str(configuration)+'_'+str(sim)+'_'+str(var)+'_'+str(reg)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(frequency)+'.ksh'
                                plot_debut=str(configuration)+'-'+str(sim)+'_'+str(plot_type)+'_'+str(loc)+'_'+str(reg)+'_'
                                plot_milieu=str(frequency)+'_'+str(var)+'_t'
                                moviename=str(plot_type)+'_'+str(loc)+'_'+str(reg)+'.'+str(frequency)+'_'+str(var)+'.mp4'
                                plotdir=params.scratch_path[machine]+'/'+str(configuration)+'/'+str(configuration)+'-'+str(sim)
                                shutil.copyfile('script_movie_'+str(machine)+'.ksh',scriptname)
                                subprocess.call(["sed", "-i", "-e",  's/CONFIGURATION/'+str(configuration)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's/SIMULATION/'+str(sim)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's/PLOT_DEBUT/'+str(plot_debut)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's/PLOT_MILIEU/'+str(plot_milieu)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's/MOVIENAME/'+str(moviename)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's/REGION/'+str(reg)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's/TYP/'+str(plot_type)+'/g', scriptname])
                                subprocess.call(["sed", "-i", "-e",  's%PLOTDIR%'+str(plotdir)+'%g', scriptname])
                                subprocess.call(["chmod", "+x", scriptname])
                                
                                with open(mpmdname, 'a') as file:
                                    file.write("{}\n".format(' ./'+str(scriptname)))
                                
    
    
    #Copy the template make for the given machine and name the make according to the specs
    subprocess.call(["chmod", "+x", mpmdname])
    subprocess.run(params.script_path[machine]+'/'+mpmdname,shell=True)


def main():
    #Import the plots definition, the script name is the argument dataset
    param_dataset = parse_args().dataset
    da = __import__(param_dataset)

    if da.make_movies == True:
        make_movies(da.machine,da.configuration,da.simulations,da.variables,da.plot_type,da.plot_locs,da.plot_regions,da.frequency,da.date_init,da.date_end)


if __name__ == "__main__":
    main()

