import cmocean
from functions import functions as f

# In the follwing replace machine, configuration, simulation, region, section and variable and fill up the dictionaries according to your setup


# Specific directories on each machine

script_path={}
script_path[machine]=PATH_TO_ATLAS

scratch_path={}
scratch_path[machine]=PATH


# Lat and lon defining the region in a plot with projection

latlon_lims={}
latlon_lims[configuration]={}
latlon_lims[configuration][region]=[X1,X2,Y1,Y2]

## All the regions we can plot in sections for each configuration

sections_name={section:SECTIONAME}

sections_list={}
sections_list[configuration]=[section]

sections_deplim={section:depth} #maximum depth along the section

sections_orientation={section:latorlon} #only straight section is supported either along lat or lon

sections_coords={}
sections_coords[configuration]={section:[A,B,C]} #A:fixed lat or lon along the section, B-C:extent along the other dimension

## All the parameters needed for a plot associated with a variable

compute={} #when a variable is a computation between several variables
compute[var]=boolean 

compute_vars={}
compute_vars[var]=[var1,var2] #the variables from which var is computed


vars_palette={var:palette} #can be cmocean.cm.xxxx or 'matplotlib_palette'

vars_unit = {var:unit} #a string, eg 'm/s'

vars_longname = {var:varlongname} #string, that will show on the plot legend

vars_vlims={}
vars_vlims[region]={var:[vmin,vmax]}

# Parameters for parallelization

mprocs={}
mprocs['map_noproj']=30
mprocs['map_orthoa']=30
mprocs['map_orthop']=30
mprocs['map_plate']=30
mprocs['map_moll']=30
mprocs['sections']=10
mprocs['time_series']=10
mprocs['hovmuller']=10
mprocs['zyplot']=5
