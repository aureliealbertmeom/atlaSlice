from functions import functions as f

# Machines list

machine_list=['adastra','jean-zay','irene','cal1','dahu']

# Directories on each machine

store_path={}
store_path['adastra']='/lus/store/CT1/hmg2840/aalbert/'
store_path['cal1']='/mnt/summer/DATA_MEOM/MODEL_SET/'
store_path['dahu']='/summer/meom/MODEL_SET'
store_path['jean-zay']='/lustre/fsstor/projects/rech/cli/rote001'

# All the configurations available on each machine

configuration_list={}
configuration_list['adastra']=['CALEDO60','eORCA36.L121','eNATL60','DFS5.2','NATL60']
configuration_list['jean-zay']=['ENS']
configuration_list['cal1']=['eNATL60']
configuration_list['dahu']=['eNATL60']

# All the simulations run with each configuration on each machine
simulation_list={}
simulation_list['adastra']={}
simulation_list['adastra']['eNATL60']=['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X','grid']
simulation_list['adastra']['CALEDO60']=['TRPC12NT0','TRPC12N00']
simulation_list['adastra']['eORCA36.L121']=['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10',
                                            'EXP22h-10','EXP09','grid']
simulation_list['adastra']['NATL60']=['CJM165']
simulation_list['adastra']['DFS5.2']=['DFS5.2']
simulation_list['cal1']={}
simulation_list['cal1']['eNATL60']=['BLBT02','BLB002']
simulation_list['dahu']={}
simulation_list['dahu']['eNATL60']=['BLBT02','BLB002']
simulation_list['jean-zay']={}
simulation_list['jean-zay']['ENS']=['04']

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory['adastra']={}
directory['adastra']['eNATL60']={}
for sim in ['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']:
    directory['adastra']['eNATL60'][sim]='/lus/store/CT1/hmg2840/brodeau/eNATL60'
directory['adastra']['eNATL60']['grid']='/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-I'
#    directory['adastra']['eNATL60'][sim]='/lus/work/CT1/hmg2840/aalbert/eNATL60' #dans le cas où je rapatrie en amont
directory['adastra']['CALEDO60']={}
directory['adastra']['CALEDO60']['TRPC12NT0']='/lus/store/CT1/ige2071/brodeau/TROPICO12/TROPICO12_NST-TRPC12NT0-S'
directory['adastra']['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    directory['adastra']['eORCA36.L121'][simu]='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-'+str(simu)+'/eORCA36.L121-'+str(simu)+'-S'
directory['adastra']['eORCA36.L121']['grid']='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I'
directory['adastra']['DFS5.2']={}
directory['adastra']['DFS5.2']['DFS5.2']='/lus/work/CT1/hmg2840/aalbert/DFS5.2_RD/ALL'
directory['adastra']['NATL60']={}
directory['adastra']['NATL60']['CJM165']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-CJM165-S'
directory['cal1']={}
directory['cal1']['eNATL60']={}
for sim in ['BLBT02','BLB002']:
    directory['cal1']['eNATL60'][sim]='/mnt/summer/DATA_MEOM/MODEL_SET/eNATL60'
directory['dahu']={}
directory['dahu']['eNATL60']={}
for sim in ['BLBT02','BLB002']:
    directory['dahu']['eNATL60'][sim]='/summer/meom/MODEL_SET/eNATL60'
directory['jean-zay']={}
directory['jean-zay']['ENS']={}
directory['jean-zay']['ENS']['04']='/lustre/fsstor/projects/rech/egi/regi700/Nemo-med/Resu/ENS04'
#directory['jean-zay']['ENS']['04']='/lustre/fsn1/projects/rech/cli/rote001/ENS/ENS-04/MED/1d'


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

stylenom['adastra']['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    stylenom['adastra']['eORCA36.L121'][simu]='aalbert_gda'

stylenom['jean-zay']={}
stylenom['jean-zay']['ENS']={}
stylenom['jean-zay']['ENS']['04']='jmb'

# All the grid files for each configuration

maskfile={}
maskfile['adastra']={}
maskfile['adastra']['eORCA36.L121']={}
maskfile['adastra']['eORCA36.L121']['eORCA36.L121']='/lus/store/CT1/hmg2840/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121_mesh_mask_noisf_v2_4.2.nc'
maskfile['adastra']['NATL60']={}
maskfile['adastra']['NATL60']['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_byte_mask.nc'
maskfile['adastra']['eNATL60']={}
maskfile['adastra']['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mask_eNATL60_3.6.nc'
for reg in ['CARA','UKFR','GULF','aGS','aLS','aMNA','PORT']:
    maskfile['adastra']['eNATL60'][reg]='/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mask_eNATL60'+str(reg)+'_3.6.nc'
maskfile['cal1']={}
maskfile['cal1']['eNATL60']={}
for reg in ['aGS','aLS','aMNA']:
	maskfile['cal1']['eNATL60'][reg]='/mnt/summer/DATA_MEOM/MODEL_SET/eNATL60/eNATL60-I/mask_eNATL60'+str(reg)+'_3.6.nc'
maskfile['dahu']={}
maskfile['dahu']['eNATL60']={}
for reg in ['aGS','aLS','aMNA']:
	maskfile['dahu']['eNATL60'][reg]='/summer/meom/MODEL_SET/eNATL60/eNATL60-I/mask_eNATL60'+str(reg)+'_3.6.nc'

bathyfile={}
bathyfile['adastra']={}
bathyfile['adastra']['eORCA36.L121']={}
bathyfile['adastra']['eORCA36.L121']['eORCA36.L121']=''
bathyfile['adastra']['NATL60']={}
bathyfile['adastra']['NATL60']['NATL60']=''
bathyfile['adastra']['eNATL60']={}
bathyfile['adastra']['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/eNATL60_BATHY_GEBCO_2014_2D_msk_v3_merg.nc4'
bathyfile['adastra']['eNATL60']['CARA']=''
bathyfile['adastra']['eNATL60']['UKFR']=''
bathyfile['adastra']['NATL60']['GULF']=''

mesh_hgr={}
mesh_hgr['adastra']={}
mesh_hgr['adastra']['NATL60']={}
mesh_hgr['adastra']['NATL60']['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_mesh_hgr.nc'
mesh_hgr['adastra']['NATL60']['GULF']='/lus/scratch/CT1/hmg2840/aalbert/NATL60/NATL60-I/NATL60GULF_v4.1_cdf_mesh_hgr.nc'
mesh_hgr['adastra']['eNATL60']={}
mesh_hgr['adastra']['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mesh_hgr_eNATL60_3.6.nc'
for reg in ['CARA','UKFR','GULF','aGS','aLS','aMNA','PORT']:
    mesh_hgr['adastra']['eNATL60'][reg]='/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mesh_hgr_eNATL60'+str(reg)+'_3.6.nc'
mesh_hgr['cal1']={}
mesh_hgr['cal1']['eNATL60']={}
for reg in ['aGS','aLS','aMNA']:
	mesh_hgr['cal1']['eNATL60'][reg]='/mnt/summer/DATA_MEOM/MODEL_SET/eNATL60/eNATL60-I/mesh_hgr_eNATL60'+str(reg)+'_3.6.nc'
mesh_hgr['dahu']={}
mesh_hgr['dahu']['eNATL60']={}
for reg in ['aGS','aLS','aMNA']:
	mesh_hgr['dahu']['eNATL60'][reg]='/summer/meom/MODEL_SET/eNATL60/eNATL60-I/mesh_hgr_eNATL60'+str(reg)+'_3.6.nc'

mesh_zgr={}
mesh_zgr['adastra']={}
mesh_zgr['adastra']['NATL60']={}
mesh_zgr['adastra']['NATL60']['NATL60']='/lus/store/CT1/hmg2840/molines/NATL60/NATL60-I/NATL60_v4.1_cdf_mesh_zgr.nc'
mesh_zgr['adastra']['NATL60']['GULF']='/lus/scratch/CT1/hmg2840/aalbert/NATL60/NATL60-I/NATL60GULF_v4.1_cdf_mesh_zgr.nc'
mesh_zgr['adastra']['eNATL60']={}
mesh_zgr['adastra']['eNATL60']['eNATL60']='/lus/store/CT1/hmg2840/brodeau/eNATL60/eNATL60-I/mesh_zgr_eNATL60_3.6.nc'
for reg in ['CARA','UKFR','GULF','aGS','aLS','aMNA','PORT']:
    mesh_zgr['adastra']['eNATL60'][reg]='/lus/work/CT1/hmg2840/aalbert/eNATL60/eNATL60-I/mesh_zgr_eNATL60'+str(reg)+'_3.6.nc'
mesh_zgr['cal1']={}
mesh_zgr['cal1']['eNATL60']={}
for reg in ['aGS','aLS','aMNA']:
	mesh_zgr['cal1']['eNATL60'][reg]='/mnt/summer/DATA_MEOM/MODEL_SET/eNATL60/eNATL60-I/mesh_zgr_eNATL60'+str(reg)+'_3.6.nc'
mesh_zgr['dahu']={}
mesh_zgr['dahu']['eNATL60']={}
for reg in ['aGS','aLS','aMNA']:
	mesh_zgr['dahu']['eNATL60'][reg]='/summer/meom/MODEL_SET/eNATL60/eNATL60-I/mesh_zgr_eNATL60'+str(reg)+'_3.6.nc'

# All the regions we can extract or plot in 2D maps for each configuration

regions_list={}
regions_list['ENS']=['MED']
regions_list['CALEDO60']=['CALEDO60']
regions_list['eNATL60']=['eNATL60','SICIL','SICILe','SICILext','CARA','UKFR','aGS','aLS','aMNA','aMNA1','aMNA2','aMNA3','aMNA4','PORT']
regions_list['NATL60']=['NATL60','GULF']
regions_list['DFS5.2']=['NATL60','eNATL60']

regions_list['eORCA36.L121']=['eORCA','global','natl','satl','arctic','antarctic','indian','windian','eindian','npac','spac','med','npole','spole','eqpac',
                              'madagascar','bassas','glorieuses','juan','tromelin','mascaraignes']

# Indices for region extraction or plots without projection corresponding to the configuration

xy={}
xy['ENS']={}
xy['ENS']['MED']=[1,566,1,264]
xy['CALEDO60']={}
xy['CALEDO60']['CALEDO60']=[0,787,0,852]

xy['eORCA36.L121']={}
xy['eORCA36.L121']['global']=[0,12959,0,10841]
xy['eORCA36.L121']['natl']=[6732,10504,6152,8924]
xy['eORCA36.L121']['satl']=[7812,11052,3436,6152]
xy['eORCA36.L121']['windian']=[11052,12959,3436,7292]
xy['eORCA36.L121']['eindian']=[0,1693,3436,7292]
xy['eORCA36.L121']['npac']=[972,7500,6152,8996]
xy['eORCA36.L121']['spac']=[2500,7812,3436,6152]
xy['eORCA36.L121']['med']=[9972,12042,7289,8400]
xy['eORCA36.L121']['eqpac']=[1972,7500,6152,6152]

xy['eNATL60']={}
xy['eNATL60']['eNATL60']=[0,8354,0,4729]
xy['eNATL60']['SICIL']=[6352,6935,1656,2311]
xy['eNATL60']['SICILext']=[6352,7035,1556,2311]
xy['eNATL60']['SICILe']=[6735,7035,1556,1876]
xy['eNATL60']['CARA']=[1,2524,1,1900]
xy['eNATL60']['UKFR']=[4652,6422,2346,4192]
#xy['eNATL60']['aGS']='-d x,1602,2286 -d y,1736,2359'
xy['eNATL60']['aGS']=[1602,2286,1736,2359]
#xy['eNATL60']['aLS']='-d x,2686,3075 -d y,3589,4274'
xy['eNATL60']['aLS']=[2686,3075,3589,4274]
#xy['eNATL60']['aMNA']='-d x,3462,4682 -d y,2337,3568'
xy['eNATL60']['aMNA']=[3462,4682,2337,3568]
xy['eNATL60']['PORT']=[4672,5282,1861,2648]
xy['eNATL60']['aMNA1']='-d x,3462,4084 -d y,2337,2965'
xy['eNATL60']['aMNA2']='-d x,4060,4682 -d y,2941,3568'
xy['eNATL60']['aMNA3']='-d x,3462,4084 -d y,2941,3568'
xy['eNATL60']['aMNA4']='-d x,4060,4682 -d y,2337,2965'
xy['NATL60']={}
xy['NATL60']['NATL60']=[0,5422,0,3454]
xy['NATL60']['GULF']=[929,1667,379,1306]


# All the variables we can extract or plot and the associated name and filetyp for each simulations

variable_list=['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE',
               'EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','MOD','VORT','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX',
               'LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','bathy','MOC','u10','v10','u10m','v10m','BOTU','BOTV','buoyancy','mask','curloverf']


vars_dim={}
for var in ['SSH','SSU','SSV','SSS','SST','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP',
            'RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX',
            'NETUPWFLX','DSALTFLX','DAMPWFLX','MOD','VORT','bathy','MOC','u10','v10','u10m','v10m','BOTU','BOTV']:
    vars_dim[var]='2D'
for var in ['T','S','U','V','W','buoyancy','curloverf']:
    vars_dim[var]='3D'


vars_name={}
vars_name['eNATL60']={}
for sim in ['BLBT02','BLB002','BLBT01','BLB001','BLBT02X','BLB002X']:
    vars_name['eNATL60'][sim]={'SSH':'sossheig','SSU':'sozocrtx','SSV':'somecrty','SST':'sosstsst','SSS':'sosaline','MLD':'somxl010',
                               'BOTU':'bozocrtx','BOTV':'bomecrty','T':'votemper','S':'vosaline','U':'vozocrtx','V':'vomecrty','W':'vovecrtz',
                               'MOC':'zomsfglo','bathy':'Bathymetry','buoyancy':'vosigma0','curloverf':'socurloverf'}
vars_name['CALEDO60']={}
for simu in ['TRPC12NT0','TRPC12N00']:
	vars_name['CALEDO60'][simu]={'SSH':'zos','SSU':'uos','SSV':'vos'}
vars_name['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10']:
    vars_name['eORCA36.L121'][simu]={'SSH':'zos','SSU':'uos','SSV':'vos','SSS':'sos','SST':'tos','U':'vozocrtx','V':'vomecrty','W':'vovecrtz',
                                     'S':'vosaline','T':'votemper','SICONC':'siconc','SITHIC':'sithic','MLD':'somxl010','TAUM':'taum','QSROCE':'qsr_oce',
                                     'QNSOCE':'qns_oce','PRECIP':'sowapre','WINDSP':'sowinsp','NETDHEATFLX':'sohefldo','SWDHEATFLX':'soshfldo',
                                     'QNS':'qns','LDHEATFLX':'solhflup','LWDHEATFLX':'solwfldo','SDHEATFLX':'sosbhfup','NETUPWFLX':'sowaflup',
                                     'DSALTFLX':'sosfldow','DAMPWFLX':'sowafld'}
vars_name['eORCA36.L121']['grid']={'bathy':'bathy_metry'}
vars_name['DFS5.2']={}
vars_name['DFS5.2']['DFS5.2']={'u10':'u10','v10':'v10'}
vars_name['NATL60']={}
vars_name['NATL60']['CJM165']={'T':'votemper','S':'vosaline'}
vars_name['ENS']={}
vars_name['ENS']['04']={}
vars_name['ENS']['04']['SSH']='sossheig'

filetyp={}
filetyp['eNATL60']={}
for sim in ['BLBT02','BLB002','BLBT02X','BLB002X']:
    filetyp['eNATL60'][sim]={'SSH':'gridT-2D','SSS':'gridT-2D','SST':'gridT-2D','MLD':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D','T':'gridT',
            'S':'gridS','U':'gridU','V':'gridV','W':'gridW','MOC':'MOC','curloverf':'curloverf'}
filetyp['eNATL60']['grid']={'bathy':'BATHY_GEBCO_2014_2D_msk_v3_merg'}
for sim in ['BLBT01','BLB001']:
    filetyp['eNATL60'][sim]={'SSH':'gridT','SSS':'gridT','SST':'gridT','SSU':'gridU','SSV':'gridV'}
filetyp['CALEDO60']={}
for simu in ['TRPC12NT0','TRPC12N00']:
	filetyp['CALEDO60'][simu]={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
filetyp['eORCA36.L121']={}
filetyp['eORCA36.L121']['grid']={'bathy':'domain_noisf_v2_4.2'}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    filetyp['eORCA36.L121'][simu]={}
    for var in ['SSH','SSS','SST','T','S','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP',
                'RHOAIR','MLD','MOD','VORT','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX']:
        filetyp['eORCA36.L121'][simu][var]='gridT'
    for var in ['SSU','U','SBU','TAUUO']:
        filetyp['eORCA36.L121'][simu][var]='gridU'
    for var in ['SSV','V','SBV','TAUVO']:
        filetyp['eORCA36.L121'][simu][var]='gridV'
    filetyp['eORCA36.L121'][simu]['W']='gridW'
    for var in ['SICONC','SITHIC']:
        filetyp['eORCA36.L121'][simu][var]='icemod'
filetyp['NATL60']={}
filetyp['NATL60']['CJM165']={'T':'gridT','S':'gridT'}
filetyp['ENS']={}
filetyp['ENS']['04']={}
filetyp['ENS']['04']['SSH']='gridTsurf_'

mask2Dname={}
mask2Dname['u10']='umaskutil'
mask2Dname['v10']='vmaskutil'

depname={}
for var in ['T','S','MOD','VORT','buoyancy']:
    depname[var]='deptht'
for var in ['U','curloverf'] :
    depname[var]='depthu'
for var in ['V'] :
    depname[var]='depthv'
for var in ['W','MOC'] :
    depname[var]='depthw'

e1name={}
for var in ['T','S','MOD','VORT','buoyancy']:
    e1name[var]='e1t'
for var in ['U','curloverf'] :
    e1name[var]='e1u'
for var in ['V'] :
    e1name[var]='e1v'
for var in ['W','MOC'] :
    e1name[var]='e1f'

e2name={}
for var in ['T','S','MOD','VORT','buoyancy']:
    e2name[var]='e2t'
for var in ['U','curloverf'] :
    e2name[var]='e2u'
for var in ['V'] :
    e2name[var]='e2v'
for var in ['W','MOC'] :
    e2name[var]='e2f'

e3name={}
for var in ['T','S','MOD','VORT','buoyancy']:
    e3name[var]='e3t_0'
for var in ['U','curloverf'] :
    e3name[var]='e3u_0'
for var in ['V'] :
    e3name[var]='e3v_0'
for var in ['W','MOC'] :
    e3name[var]='e3w_0'

varpt={'T':'T','S':'T','SSH':'T','SST':'T','SSS':'T','SSU':'U','SSV':'V','U':'U','V':'V','W':'W','TAUM':'T','TAUBOT':'T','QTOCE':'T','QSROCE':'T',
       'QSBOCE':'T','QNSOCE':'T','QLWOCE':'T','QLAOCE':'T','PRECIP':'T','EVAPOCE':'T','EMPMR':'T','WINDSP':'T','RHOAIR':'T','MLD':'T','BOTU':'U',
       'TAUUO':'U','BOTV':'V','TAUVO':'V','u10':'U','v10':'V','u10m':'U','v10m':'V','curloverf':'U'}


compute={}
for var in ['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE',
            'EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX',
            'SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','MOC','u10','v10']:
    compute[var]=False
for var in ['MOD','VORT']:
    compute[var]=True

compute_vars={}
for var in ['MOD','VORT']:
    compute_vars[var]=['U','V']

# The time frequency available for a given variable and simulation

frequencies={}
frequencies['ENS']={}
frequencies['ENS']['04']={'SSH':'1d'}
frequencies['eNATL60']={}
for simu in ['BLB002','BLBT02','BLB002X','BLBT02X']:
    frequencies['eNATL60'][simu]={'MOC':'1h','SSH':'1h','SSS':'1h','SST':'1h','SSU':'1h','SSV':'1h','T':'1h','S':'1h','U':'1h','V':'1h','W':'1h','curloverf':'1h'}
frequencies['CALEDO60']={}
frequencies['CALEDO60']['TRPC12NT0']={'SSH':'1h','SSU':'1h','SSV':'1h'}
frequencies['CALEDO60']['TRPC12N00']={'SSH':'1h','SSU':'1h','SSV':'1h'}
frequencies['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    frequencies['eORCA36.L121'][simu]={'SSH':'1h','SSU':'1h','SSV':'1h','SSS':'1h','SST':'1h','MLD':'1h','SICONC':'1h','SITHIC':'1h','MOD':'1h','VORT':'1h','U':'12h','V':'12h','S':'12h','T':'12h','W':'12h','NETDHEATFLX':'1h','NETUPWFLX':'1h','PRECIP':'1h','WINDSP':'1h','SWDHEATFLX':'1h','LWDHEATFLX':'1h'}

frequencies_file={}
frequencies_file['ENS']={}
frequencies_file['ENS']['04']={}
frequencies_file['ENS']['04']['SSH']='2y'
#frequencies_file['ENS']['04']['SSH']='1d'
frequencies_file['eNATL60']={}
for simu in ['BLB002','BLBT02','BLB002X','BLBT02X']:
    frequencies_file['eNATL60'][simu]={'MOC':'1d','SSH':'1d','SSS':'1d','SST':'1d','SSU':'1d','SSV':'1d','T':'1d','S':'1d','U':'1d','V':'1d','W':'1d','curloverf':'1d'}
frequencies_file['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    frequencies_file['eORCA36.L121'][simu]={'NETDHEATFLX':'12h','NETUPWFLX':'12h','PRECIP':'12h','WINDSP':'12h','SWDHEATFLX':'12h','LWDHEATFLX':'12h',
                     'SSH':'12h','SSU':'12h','SSV':'12h','SSS':'12h','SST':'12h','MLD':'12h','SICONC':'12h','SITHIC':'12h','MOD':'12h','VORT':'12h',
                     'U':'12h','V':'12h','S':'12h','T':'12h','W':'12h'}

# The period of time covered by a simulation

sim_date_init={}
sim_date_end={}
sim_date_init['CALEDO60']={}
sim_date_end['CALEDO60']={}
for sim in ['TRPC12NT0','TRPC12N00']:
    sim_date_init['CALEDO60'][sim]='2012-01-01'
    sim_date_end['CALEDO60'][sim]='2018-12-31'

sim_date_init['eNATL60']={}
sim_date_end['eNATL60']={}
for sim in ['BLBT02','BLB002']:
    sim_date_init['eNATL60'][sim]='2009-06-30'
sim_date_end['eNATL60']['BLB002']='2009-11-16'
sim_date_end['eNATL60']['BLBT02']='2009-11-06'

sim_date_init['eNATL60']['BLB002X']='2009-11-17'
sim_date_end['eNATL60']['BLB002X']='2010-07-31'
sim_date_init['eNATL60']['BLBT02X']='2009-11-07'
sim_date_end['eNATL60']['BLBT02X']='2010-10-29'
sim_date_init['eNATL60']['BLB001']='2009-01-01'
sim_date_end['eNATL60']['BLB001']='2009-06-29'

sim_date_init['eORCA36.L121']={}
for simu in ['EXP13-10','EXP09']:
    sim_date_init['eORCA36.L121'][simu]='2017-01-01 11:00'
for simu in ['EXP15-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10']:
    sim_date_init['eORCA36.L121'][simu]='2012-01-01 11:00'

sim_date_end['eORCA36.L121']={}
sim_date_end['eORCA36.L121']['EXP13-10']='2017-01-03 23:00'
sim_date_end['eORCA36.L121']['EXP15-10']='2012-02-22 23:00'
for simu in ['EXP22a-10','EXP22b-10','EXP22c-10','EXP22f-10','EXP22g-10','EXP22h-10']:
    sim_date_end['eORCA36.L121'][simu]='2012-01-01 11:00'
for simu in ['EXP22d-10','EXP22e-10']:
    sim_date_end['eORCA36.L121'][simu]='2012-01-01 23:00'

sim_date_init['DFS5.2']={}
sim_date_end['DFS5.2']={}
sim_date_init['DFS5.2']['DFS5.2']='1958'
sim_date_end['DFS5.2']['DFS5.2']='2015'
sim_date_init['NATL60']={}
sim_date_end['NATL60']={}
sim_date_init['NATL60']['CJM165']='2012-06-14'
sim_date_end['NATL60']['CJM165']='2013-10-01'
sim_date_init['ENS']={}
sim_date_end['ENS']={}
sim_date_init['ENS']['04']='1979-06-27'
sim_date_end['ENS']['04']='2020-12-27'
