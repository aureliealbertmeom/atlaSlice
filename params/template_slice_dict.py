# In the following replace machine, configuration, simulation, region and variable and fill up the dictionaries according to your setup

# Directories for soecific tools on each machine

nco_path={}
nco_path[machine]=PATH_TO_NCO_BIN

cdf_path={}
cdf_path[machine]=PATH_TO_CDFTOOLS_BIN

sosie_path={}
sosie_path[machine]=PATH_TO_SOSIE

# Name of extractions in short

ex={}
ex[configuration]={}
ex[configuration][configuration]='' #when we extract the whole domain we do not change the name
ex[configuration][region]=regionshort #in the case the region name is too long

# Parameters for parallelization

mprocs={}
mprocs['apply_mask']=30
mprocs['project_sosie']=30
mprocs['daily_files']=30
mprocs['daily_mean']=30
mprocs['degrad']=30
mprocs['extract']=10
