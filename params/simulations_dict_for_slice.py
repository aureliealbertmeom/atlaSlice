
# Machines list

machine_list=['adastra','jean-zay','irene']

# Directories on each machine

script_path={}
script_path['adastra']='/lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice'

nco_path={}
nco_path['adastra']='/lus/home/CT1/hmg2840/aalbert/.conda/envs/nco/bin'

cdf_path={}
cdf_path['adastra']='/lus/work/CT1/hmg2840/aalbert/git/CDFTOOLS/bin/'

sosie_path={}
sosie_path['adastra']='/lus/work/CT1/hmg2840/aalbert/DEV/sosie'

scratch_path={}
scratch_path['adastra']='/lus/scratch/CT1/hmg2840/aalbert/TMPEXTRACT'

store_path={}
store_path['adastra']='/lus/store/CT1/hmg2840/aalbert/'

# All the configurations available on each machine

configuration_list={}
configuration_list['adastra']=['CALEDO60','eNATL60','DFS5.2','NATL60']

# All the simulations run with each configuration on each machine

simulation_list={}
simulation_list['adastra']={}
simulation_list['adastra']['CALEDO60']=['TRPC12NT0','TRPC12N00']
simulation_list['adastra']['eNATL60']=['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']
simulation_list['adastra']['NATL60']=['CJM165']
simulation_list['adastra']['DFS5.2']=['DFS5.2']

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory['adastra']={}
directory['adastra']['CALEDO60']={}
directory['adastra']['CALEDO60']['TRPC12NT0']='/lus/store/CT1/hmg2840/brodeau/TROPICO12/TROPICO12_NST-TRPC12NT0-S'
directory['adastra']['eNATL60']={}
for sim in ['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']:
    directory['adastra']['eNATL60'][sim]='/lus/store/CT1/hmg2840/brodeau/eNATL60'
#    directory['adastra']['eNATL60'][sim]='/lus/work/CT1/hmg2840/aalbert/eNATL60' #dans le cas où je rapatrie en amont
directory['adastra']['DFS5.2']={}
directory['adastra']['DFS5.2']['DFS5.2']='/lus/work/CT1/hmg2840/aalbert/DFS5.2_RD/ALL'
directory['adastra']['NATL60']={}
directory['adastra']['NATL60']['CJM165']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-CJM165-S'

stylenom={}
stylenom['adastra']={}
stylenom['adastra']['CALEDO60']={}
stylenom['adastra']['CALEDO60']['TRPC12NT0']='brodeau_nst'
stylenom['adastra']['DFS5.2']={}
stylenom['adastra']['DFS5.2']['DFS5.2']='dfs'
stylenom['adastra']['eNATL60']={}
for sim in ['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']:
    stylenom['adastra']['eNATL60'][sim]='brodeau_enatl'
for sim in ['BLBT01','BLB001']:
    stylenom['adastra']['eNATL60'][sim]='brodeau_enatl_spinup'
stylenom['adastra']['NATL60']={}
for sim in ['CJM165']:
    stylenom['adastra']['NATL60'][sim]='molines'

# All the regions we can extract in a configuration and the associated parameters

regions_list={}
regions_list['CALEDO60']=['CALEDO60']
regions_list['eNATL60']=['eNATL60','SICIL','SICILe','SICILext','CARA','UKFR']
regions_list['NATL60']=['NATL60','GULF']
regions_list['DFS5.2']=['NATL60','eNATL60']

xy={}
xy['CALEDO60']={}
xy['CALEDO60']['CALEDO60']=''
xy['eNATL60']={}
xy['eNATL60']['eNATL60']=''
xy['eNATL60']['SICIL']='-d x,6352,6935 -d y,1656,2311'
xy['eNATL60']['SICILext']='-d x,6352,7035 -d y,1556,2311'
xy['eNATL60']['SICILe']='-d x,6735,7035 -d y,1556,1876'
xy['eNATL60']['CARA']='-d x,1,2524 -d y,1,1900'
xy['eNATL60']['UKFR']='-d x,4652,6422 -d y,2346,4192'
xy['eNATL60']['aGS']='-d x,1614,2274 -d y,1748,2347'
xy['eNATL60']['aLS']='-d x,2698,3063 -d y,3601,4262'
xy['eNATL60']['aMNA']='-d x,3474,4670 -d y,2349,3556'
xy['NATL60']={}
xy['NATL60']['NATL60']=''
xy['NATL60']['GULF']='-d x,929,1667 -d y,379,1306'

ex={}
ex['CALEDO60']={}
ex['CALEDO60']['CALEDO60']=''
ex['eNATL60']={}
ex['eNATL60']['eNATL60']=''
ex['eNATL60']['SICIL']='SICIL'
ex['eNATL60']['SICILext']='SICILext'
ex['eNATL60']['SICILe']='SICILe'
ex['eNATL60']['CARA']='CARA'
ex['eNATL60']['UKFR']='UKFR'
ex['eNATL60']['aGS']='aGS'
ex['eNATL60']['aLS']='aLS'
ex['eNATL60']['aMNA']='aMNA'
ex['DFS5.2']={}
ex['DFS5.2']['NATL60']='NATL60'
ex['DFS5.2']['eNATL60']='eNATL60'
ex['NATL60']={}
ex['NATL60']['NATL60']=''
ex['NATL60']['GULF']='GULF'

mask={}
mask['NATL60']={}
mask['NATL60']['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_byte_mask.nc'
mask['eNATL60']={}
mask['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mask_eNATL60_3.6.nc'
mask['eNATL60']['CARA']='/lus/scratch/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mask_eNATL60CARA_3.6.nc'
mask['eNATL60']['UKFR']='/lus/scratch/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mask_eNATL60UKFR_3.6.nc'
mask['NATL60']['GULF']='/lus/scratch/CT1/hmg2840/aalbert/NATL60/NATL60-I/NATL60GULF_v4.1_cdf_byte_mask.nc'

mesh_hgr={}
mesh_hgr['NATL60']={}
mesh_hgr['NATL60']['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_mesh_hgr.nc'
mesh_hgr['eNATL60']={}
mesh_hgr['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mesh_hgr_eNATL60_3.6.nc'
mesh_hgr['eNATL60']['CARA']='/lus/scratch/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mesh_hgr_eNATL60CARA_3.6.nc'
mesh_hgr['eNATL60']['UKFR']='/lus/scratch/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mesh_hgr_eNATL60UKFR_3.6.nc'
mesh_hgr['NATL60']['GULF']='/lus/scratch/CT1/hmg2840/aalbert/NATL60/NATL60-I/NATL60GULF_v4.1_cdf_mesh_hgr.nc'
mesh_zgr={}
mesh_zgr['NATL60']={}
mesh_zgr['NATL60']['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_mesh_zgr.nc'
mesh_zgr['eNATL60']={}
mesh_zgr['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mesh_zgr_eNATL60_3.6.nc'
mesh_zgr['eNATL60']['CARA']='/lus/scratch/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mesh_zgr_eNATL60CARA_3.6.nc'
mesh_zgr['eNATL60']['UKFR']='/lus/scratch/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mesh_zgr_eNATL60UKFR_3.6.nc'
mesh_zgr['NATL60']['GULF']='/lus/scratch/CT1/hmg2840/aalbert/NATL60/NATL60-I/NATL60GULF_v4.1_cdf_mesh_zgr.nc'

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
for sim in ['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']:
    vars_name[sim]={'SSH':'sossheig','SSU':'sozocrtx','SSV':'somecrty','SST':'sosstsst','SSS':'sosaline','MLD':'somxl010','BOTU':'bozocrtx','BOTV':'bomecrty','T':'votemper','S':'vosaline','U':'vozocrtx','V':'vomecrty','W':'vovecrtz'}
vars_name['DFS5.2']={'u10':'u10','v10':'v10'}
vars_name['CJM165']={'T':'votemper','S':'vosaline'}

filetyp={}
for sim in ['TRPC12NT0','TRPC12N00']:
    filetyp[sim]={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
for sim in ['BLBT02','BLB002','BLBT02X','BLB002X']:
    filetyp[sim]={'SSH':'gridT-2D','SSS':'gridT-2D','SST':'gridT-2D','MLD':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D','T':'gridT','S':'gridS','U':'gridU','V':'gridV','W':'gridW'}
for sim in ['BLBT01','BLB001']:
    filetyp[sim]={'SSH':'gridT','SSS':'gridT','SST':'gridT','SSU':'gridU','SSV':'gridV'}
filetyp['CJM165']={'T':'gridT','S':'gridT'}

varpt={'T':'T','S':'T','SSH':'T','SST':'T','SSS':'T','SSU':'U','SSV':'V','U':'U','V':'V','W':'W','TAUM':'T','TAUBOT':'T','QTOCE':'T','QSROCE':'T','QSBOCE':'T','QNSOCE':'T','QLWOCE':'T','QLAOCE':'T','PRECIP':'T','EVAPOCE':'T','EMPMR':'T','WINDSP':'T','RHOAIR':'T','MLD':'T','BOTU':'U','TAUUO':'U','BOTV':'V','TAUVO':'V','u10':'U','v10':'V','u10m':'U','v10m':'V'}

vars_dim={'SSH':'2D','SST':'2D','SSS':'2D','SSU':'2D','SSV':'2D','T':'3D','S':'3D','U':'3D','V':'3D','W':'3D','TAUM':'2D','TAUBOT':'2D','QTOCE':'2D','QSROCE':'2D','QSBOCE':'2D','QNSOCE':'2D','QLWOCE':'2D','QLAOCE':'2D','PRECIP':'2D','EVAPOCE':'2D','EMPMR':'2D','WINDSP':'2D','RHOAIR':'2D','MLD':'2D','BOTU':'2D','TAUUO':'2D','BOTV':'2D','TAUVO':'2D','u10':'2D','v10':'2D','u10m':'2D','v10m':'2D'}

# The time frequency available for a given variable and simulation
frequencies={}
for sim in ['TRPC12NT0','TRPC12N00']:
    frequencies[sim]={'SSH':'1h','SSU':'1h','SSV':'1h'}
for sim in ['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']:
    frequencies[sim]={'SSH':'1h','SSS':'1h','SST':'1h','SSU':'1h','SSV':'1h','T':'1h','S':'1h'}
frequencies['DFS5.2']={'u10':'3h','v10':'3h'}
frequencies['CJM165']={'T':'1d','S':'1d'}

# The time frequency of the output file foa given var and sim
file_frequencies={}
for sim in ['TRPC12NT0','TRPC12N00']:
    file_frequencies[sim]={'SSH':'1m','SSU':'1m','SSV':'1m'}
for sim in ['BLBT02','BLB002','BLBT02X','BLB002X']:
    file_frequencies[sim]={'SSH':'1d','SSS':'1d','SST':'1d','SSU':'1d','SSV':'1d','T':'1d','S':'1d'}
for sim in ['BLBT01','BLB001']:
    file_frequencies[sim]={'SSH':'5d'}
file_frequencies['DFS5.2']={'u10':'1y','v10':'1y'}
file_frequencies['CJM165']={'T':'1d','S':'1d'}

# The period of time covered by a simulation
sim_date_init={}
sim_date_end={}
for sim in ['TRPC12NT0','TRPC12N00']:
    sim_date_init[sim]='2012-01-01'
    sim_date_end[sim]='2018-12-31'
for sim in ['BLBT02','BLB002']:
    sim_date_init[sim]='2009-06-30'
sim_date_end['BLB002']='2009-11-16'
sim_date_init['BLB002X']='2009-11-17'
sim_date_end['BLB002X']='2010-07-31'
sim_date_end['BLBT02']='2009-11-06'
sim_date_init['BLBT02X']='2009-11-07'
sim_date_end['BLBT02X']='2010-10-29'
sim_date_init['BLB001']='2009-01-01'
sim_date_end['BLB001']='2009-06-29'
sim_date_init['DFS5.2']='1958'
sim_date_end['DFS5.2']='2015'
sim_date_init['CJM165']='2012-06-14'
sim_date_end['CJM165']='2013-10-01'


mprocs={}
mprocs['apply_mask']=30
mprocs['project_sosie']=30
mprocs['daily_files']=30
mprocs['daily_mean']=30
mprocs['degrad']=30
mprocs['extract']=10

