
# Machines list

machine_list=['adastra','jean-zay','irene']

# Directories on each machine

script_path={}
script_path['adastra']='/lus/home/CT1/ige2071/aalbert/git/atlas/slice'

nco_path={}
nco_path['adastra']='/lus/home/CT1/ige2071/aalbert/.conda/envs/nco/bin'

cdf_path={}
cdf_path['adastra']='/lus/work/CT1/ige2071/aalbert/git/CDFTOOLS/bin/'

sosie_path={}
sosie_path['adastra']='/lus/work/CT1/hmg2840/aalbert/DEV/sosie'

scratch_path={}
scratch_path['adastra']='/lus/scratch/CT1/hmg2840/aalbert/TMPEXTRACT'

store_path={}
store_path['adastra']='/lus/store/CT1/hmg2840/aalbert/'

# All the configurations available on each machine

configuration_list={}
configuration_list['adastra']=['CALEDO60','eNATL60','DFS5.2']

# All the simulations run with each configuration on each machine

simulation_list={}
simulation_list['adastra']={}
simulation_list['adastra']['CALEDO60']=['TRPC12NT0','TRPC12N00']
simulation_list['adastra']['eNATL60']=['BLBT02','BLB002']
simulation_list['adastra']['DFS5.2']=['DFS5.2']

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory['adastra']={}
directory['adastra']['CALEDO60']={}
directory['adastra']['CALEDO60']['TRPC12NT0']='/lus/store/CT1/ige2071/brodeau/TROPICO12/TROPICO12_NST-TRPC12NT0-S'
directory['adastra']['eNATL60']={}
directory['adastra']['eNATL60']['BLBT02']='/lus/store/CT1/hmg2840/brodeau/eNATL60'
directory['adastra']['eNATL60']['BLB002']='/lus/store/CT1/hmg2840/brodeau/eNATL60'
directory['adastra']['DFS5.2']={}
directory['adastra']['DFS5.2']['DFS5.2']='/lus/work/CT1/hmg2840/aalbert/DFS5.2_RD/ALL'

stylenom={}
stylenom['adastra']={}
stylenom['adastra']['CALEDO60']={}
stylenom['adastra']['CALEDO60']['TRPC12NT0']='brodeau_nst'
stylenom['adastra']['DFS5.2']={}
stylenom['adastra']['DFS5.2']['DFS5.2']='dfs'
stylenom['adastra']['eNATL60']={}
for sim in ['BLBT02','BLB002']:
    stylenom['adastra']['eNATL60'][sim]='brodeau_enatl'

# All the regions we can extract in a configuration and the associated parameters

regions_list={}
regions_list['CALEDO60']=['CALEDO60']
regions_list['eNATL60']=['eNATL60','SICIL']
regions_list['DFS5.2']=['NATL60','eNATL60']

xy={}
xy['CALEDO60']={}
xy['CALEDO60']['CALEDO60']=''
xy['eNATL60']={}
xy['eNATL60']['eNATL60']=''
xy['eNATL60']['SICIL']='-d x,6352,6935 -d y,1656,2311'

ex={}
ex['CALEDO60']={}
ex['CALEDO60']['CALEDO60']=''
ex['eNATL60']={}
ex['eNATL60']['eNATL60']=''
ex['eNATL60']['SICIL']='SICIL'
ex['DFS5.2']={}
ex['DFS5.2']['NATL60']='NATL60'
ex['DFS5.2']['eNATL60']='eNATL60'

mask={}
mask['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_byte_mask.nc'
mask['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mask_eNATL60_3.6.nc'

mask2Dname={}
mask2Dname['u10']='umaskutil'
mask2Dname['v10']='vmaskutil'

depname={}
for var in ['T','S','MOD','VORT']:
    depname[var]='deptht'
for var in ['U'] :
    depname[var]='depthu'
for var in ['V'] :
    depname[var]='depthv'
for var in ['W'] :
    depname[var]='depthw'

# All the variables we can extract and the associated name and filetyp for each simulations

variable_list=['SSH','SSU','SSV','SST','SSS','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','u10','v10']

vars_name={}
for sim in ['TRPC12NT0','TRPC12N00']:
    vars_name[sim]={'SSH':'z s','SSU':'uos','SSV':'vos'}
for sim in ['BLBT02','BLB002']:
    vars_name[sim]={'SSH':'sossheig','SSU':'sozocrtx','SSV':'somecrty','SST':'sosstsst','SSS':'sosaline','MLD':'somxl010','BOTU':'bozocrtx','BOTV':'bomecrty','T':'votemper','S':'vosaline','U':'vozocrtx','V':'vomecrty','W':'vovecrtz'}
vars_name['DFS5.2']={'u10':'u10','v10':'v10'}

filetyp={}
for sim in ['TRPC12NT0','TRPC12N00']:
    filetyp[sim]={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
for sim in ['BLBT02','BLB002']:
    filetyp[sim]={'SSH':'gridT-2D','SSS':'gridT-2D','SST':'gridT-2D','MLD':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D','T':'gridT'}

vars_dim={'SSH':'2D','SST':'2D','SSS':'2D','SSU':'2D','SSV':'2D','T':'3D','S':'3D','U':'3D','V':'3D','W':'3D','TAUM':'2D','TAUBOT':'2D','QTOCE':'2D','QSROCE':'2D','QSBOCE':'2D','QNSOCE':'2D','QLWOCE':'2D','QLAOCE':'2D','PRECIP':'2D','EVAPOCE':'2D','EMPMR':'2D','WINDSP':'2D','RHOAIR':'2D','MLD':'2D','BOTU':'2D','TAUUO':'2D','BOTV':'2D','TAUVO':'2D','u10':'2D','v10':'2D','u10m':'2D','v10m':'2D'}

# The time frequency available for a given variable and simulation
frequencies={}
for sim in ['TRPC12NT0','TRPC12N00']:
    frequencies[sim]={'SSH':'1h','SSU':'1h','SSV':'1h'}
for sim in ['BLBT02','BLB002']:
    frequencies[sim]={'SSH':'1h','SSS':'1h','SST':'1h','SSU':'1h','SSV':'1h','T':'1h'}
frequencies['DFS5.2']={'u10':'3h','v10':'3h'}

# The time frequency of the output file foa given var and sim
file_frequencies={}
for sim in ['TRPC12NT0','TRPC12N00']:
    file_frequencies[sim]={'SSH':'1m','SSU':'1m','SSV':'1m'}
for sim in ['BLBT02','BLB002']:
    file_frequencies[sim]={'SSH':'1d','SSS':'1d','SST':'1d','SSU':'1d','SSV':'1d','T':'1d'}
file_frequencies['DFS5.2']={'u10':'1y','v10':'1y'}

# The period of time covered by a simulation
sim_date_init={}
sim_date_end={}
for sim in ['TRPC12NT0','TRPC12N00']:
    sim_date_init[sim]='2012-01-01'
    sim_date_end[sim]='2018-12-31'
for sim in ['BLBT02','BLB002']:
    sim_date_init[sim]='2009-07-01'
    sim_date_end[sim]='2010-06-30'
sim_date_init['DFS5.2']='1958'
sim_date_end['DFS5.2']='2015'


mprocs={}
mprocs['apply_mask']=30
mprocs['project_sosie']=30
mprocs['daily_files']=30
mprocs['daily_mean']=30

