#! /usr/bin/env python

import sys,getopt,os,glob
import argparse
import pandas as pd
import subprocess

#Make sure the path to the package is in the PYTHONPATH
from slice import functions as f
from params import simulations_dict_for_slice as params

def parse_args():
    parser=argparse.ArgumentParser(description="check if the requested extractions defined in dataset have been performed")
    parser.add_argument('-param',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check(machine,configuration,simulations,regions,variables,frequency,date_init,date_end):

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
            tdir=str(params.scratch_path[machine])+'/'+str(configuration)+'/'+str(configuration)+'-'+str(simulation)+'/'+str(region)+'/'+str(frequency)
            nb_files_obtained=len([name for name in os.listdir(tdir) if os.path.isfile(tdir+'/'+name)])
            print(str(nb_files_obtained)+' out of '+str(nb_files_expected)+' files were extracted for simulation '+str(simulation)+' and region '+str(region)+' in '+str(tdir))

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



def main():
    param_dataset = parse_args().param
    da = __import__(param_dataset)

    print('Extractions for '+str(param_dataset)+' are checked')
    check(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end)

    if da.operation == '1d-mean':
        check(da.machine,da.configuration,da.simulations,da.regions,da.variables,'1d',da.date_init,da.date_end)

if __name__ == "__main__":
    main()

