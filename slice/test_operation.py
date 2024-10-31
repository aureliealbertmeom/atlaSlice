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


def one_operation(machine,configuration,simulations,regions,variables,frequency,date_init,date_end,operation):

    var=variables[0]

    #Determine the frequency of parallelization
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

    ym=incr_temp[0]
    year=ym.year
    month=ym.month
    mm="{:02d}".format(month)
    if freq_par == '1m':
        tag=str(year)+'-'+str(mm)
    if freq_par == '1d':
        day=ym.day
        dd="{:02d}".format(day)
        tag=str(year)+'-'+str(mm)+'-'+str(dd)

    simulation=simulations[0]
    region=regions[0]
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

    subprocess.call(["chmod", "+x", scriptname])
    subprocess.run(params.script_path[machine]+'/'+scriptname,shell=True)

def main():
    param_dataset = parse_args().param
    da = __import__(param_dataset)

    print('One operation '+str(da.operation)+' for '+str(param_dataset)+' is launched')
    one_operation(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end,da.operation)


if __name__ == "__main__":
    main()
