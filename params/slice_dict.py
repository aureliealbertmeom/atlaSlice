
# Directories for soecific tools on each machine

nco_path={}
nco_path['adastra']='/lus/home/CT1/hmg2840/aalbert/.conda/envs/nco/bin'

cdf_path={}
cdf_path['adastra']='/lus/work/CT1/hmg2840/aalbert/git/CDFTOOLS/bin/'

sosie_path={}
sosie_path['adastra']='/lus/work/CT1/hmg2840/aalbert/DEV/sosie'

# Name of extractions in short

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
ex['DFS5.2']={}
ex['DFS5.2']['NATL60']='NATL60'
ex['DFS5.2']['eNATL60']='eNATL60'
ex['NATL60']={}
ex['NATL60']['NATL60']=''
ex['NATL60']['GULF']='GULF'

# Parameters for parallelization

mprocs={}
mprocs['apply_mask']=30
mprocs['project_sosie']=30
mprocs['daily_files']=30
mprocs['daily_mean']=30
mprocs['degrad']=30
mprocs['extract']=10
