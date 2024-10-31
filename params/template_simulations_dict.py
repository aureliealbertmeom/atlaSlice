from functions import functions as f


# In the following replace machine, configuration, simulation, region and variable and fill up the dictionaries according to your setup

# Machines list

machine_list=[machine]

# Directories on each machine

script_path={}
script_path[machine]=PATH

scratch_path={}
scratch_path[machine]=PATH

store_path={}
store_path[machine]=PATH

# All the configurations available on each machine

configuration_list={}
configuration_list[machine]=[configuration]

# All the simulations run with each configuration on each machine
simulation_list={}
simulation_list[machine]={}
simulation_list[machine][configuration]=[simulation]

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory[machine]={}
directory[machine][configuration]={}
directory[machine][configuration][simiulation]=PATH

# How the name of files are built and the architecture of storage
stylenom={}
stylenom[machine]={}
stylenom[machine][configuration]={}
stylenom[machine][configuration][sim]=style # only brodeau_nst, brodeau_enatl, brodeau_enatl_spinup, molines, aalbert_gda and dfs are possible

# All the grid files for each configuration

maskfile={}
maskfile[machine]={}
maskfile[machine][configuration]={}
maskfile[machine][configuration][configuration]=PATH/FILE #grid files for the whole configuration
maskfile[machine][configuration][region]=PATH/FILE #grid files for the extracted region

mesh_hgr={}
mesh_hgr[machine]={}
mesh_hgr[machine][configuration]={}
mesh_hgr[machine][configuration][configuration]=PATH/FILE

mesh_zgr={}
mesh_zgr[machine]={}
mesh_zgr[machine][configuration]={}
mesh_zgr[machine][configuration][configuration]=PATH/FILE

# All the regions we can extract or plot in 2D maps for each configuration

regions_list={}
regions_list[configuration]=[configuration,region]

# Indices for region extraction or plots without projection corresponding to the configuration

xy={}
xy[configuration]={}
xy[configuration][configuration]=[X1,X2,Y1,Y2] #for plots or extraction of the whole domain
xy[configuration][region]=[X1,X2,Y1,Y2]


# All the variables we can extract or plot and the associated name and filetyp for each simulations

variable_list=var

vars_dim={}
vars_dim[var]=XD

vars_name={}
vars_name[configuration]={}
vars_name[configuration][simulation]={var:varname_in_file}

filetyp={}
filetyp[configuration]={}
filetyp[configuration][simulation]={var:filetype} #ex: gridT, icemod, gridU-2D

mask2Dname={var:maskvar} #if needed, ex umaskutil

depname={var:depthvar} #if needed, ex deptht

varpt={var:X} #if needed, ex T, F

# The time frequency available for a given variable and simulation

frequencies={}
frequencies[configuration]={}
frequencies[configuration][simulation]={var:frequency} #ex 1h, 5d

frequencies_file={}
frequencies_file[configuration]={}
frequencies_file[configuration][simulation]={var:frequency} #concat frequency

# The period of time covered by a simulation

sim_date_init={}
sim_date_end={}
sim_date_init[configuration]={}
sim_date_end[configuration]={}
sim_date_init[configuration][simulation]=date #ex '2009-01-01 00:00'
sim_date_end[configuration][simulation]=date #ex '2009-01-01 00:00'

