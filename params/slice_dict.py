
# Directories for soecific tools on each machine

script_path={}
script_path['adastra']='/lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice'

params_path={}
params_path['adastra']='/lus/home/CT1/hmg2840/aalbert/git/atlaSlice/params'

nco_path={}
nco_path['adastra']='/opt/software/gaia/prod/3.2.0/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_plac/nco-5.1.9-gcc-12.1.generic-3z7d/bin/'

cdf_path={}
cdf_path['adastra']='/lus/work/CT1/hmg2840/aalbert/git/CDFTOOLS/bin/'

sosie_path={}
sosie_path['adastra']='/lus/work/CT1/hmg2840/aalbert/DEV/sosie'

scratch_path={}
#scratch_path['adastra']='/lus/store/CT1/hmg2840/aalbert'
scratch_path['adastra']='/lus/work/CT1/hmg2840/aalbert'
#scratch_path['adastra']='/lus/scratch/CT1/hmg2840/aalbert/TMPEXTRACT'

# Name of extractions in short

ex={}
ex['CALEDO60']={}
ex['CALEDO60']['CALEDO60']=''
ex['eNATL60']={}
ex['eNATL60']['eNATL60']=''
for reg in ['SICIL','SICILext','SICILe','CARA','UKFR','aGS','aLS','aMNA','aMNA1','aMNA2','aMNA3','aMNA4','PORT']:
    ex['eNATL60'][reg]=str(reg)
ex['DFS5.2']={}
ex['DFS5.2']['NATL60']='NATL60'
ex['DFS5.2']['eNATL60']='eNATL60'
ex['NATL60']={}
ex['NATL60']['NATL60']=''
ex['NATL60']['GULF']='GULF'

# Parameters for profiles in 1°x1° boxes

nb_boxes={}
nb_boxes['eNATL60']={}
nb_boxes['eNATL60']['aGS']=109
nb_boxes['eNATL60']['aLS']=65
nb_boxes['eNATL60']['aMNA']=399

# Parameters for parallelization

mprocs={}
mprocs['apply_mask']=30
mprocs['project_sosie']=30
mprocs['daily_files']=30
mprocs['daily_mean']=30
mprocs['degrad']=30
mprocs['extract']=10
mprocs['compute_buoyancy']=10
mprocs['compute_curl']=10
