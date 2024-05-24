import cmocean
import atlas.functions as f

# Machines list

machine_list=['adastra','jean-zay','irene']

# Directories on each machine

script_path={}
script_path['adastra']='/lus/home/CT1/ige2071/aalbert/git/atlas/scripts'

scratch_path={}
scratch_path['adastra']='/lus/scratch/CT1/hmg2840/aalbert/TMPPLOTS'

store_path={}
store_path['adastra']='/lus/store/CT1/hmg2840/aalbert/'

# All the configurations available on each machine

configuration_list={}
configuration_list['adastra']=['CALEDO60','eORCA36.L121']

# All the simulations run with each configuration on each machine
simulation_list={}
simulation_list['adastra']={}
simulation_list['adastra']['CALEDO60']=['TRPC12NT0','TRPC12N00']
simulation_list['adastra']['eORCA36.L121']=['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09','grid']

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory['adastra']={}
directory['adastra']['CALEDO60']={}
directory['adastra']['CALEDO60']['TRPC12NT0']='/lus/store/CT1/ige2071/brodeau/TROPICO12/TROPICO12_NST-TRPC12NT0-S'

directory['adastra']['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    directory['adastra']['eORCA36.L121'][simu]='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-'+str(simu)+'/eORCA36.L121-'+str(simu)+'-S'
directory['adastra']['eORCA36.L121']['grid']='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I'


stylenom={}
stylenom['adastra']={}
stylenom['adastra']['CALEDO60']={}
stylenom['adastra']['CALEDO60']['TRPC12NT0']='brodeau_nst'

stylenom['adastra']['eORCA36.L121']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    stylenom['adastra']['eORCA36.L121'][simu]='aalbert_gda'

maskfile={}
maskfile['adastra']={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','grid']:
    maskfile['adastra'][simu]='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121_mesh_mask_noisf_v2_4.2.nc'
maskfile['adastra']['EXP09']='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121-MAA2023_mesh_mask_v4_4.2.nc'
# All the regions we can plot in 2D maps for each configuration

regions_list={}
regions_list['CALEDO60']=['caledo']

regions_list['eORCA36.L121']=['global','natl','satl','arctic','antarctic','indian','windian','eindian','npac','spac','med','npole','spole','eqpac','madagascar','bassas','glorieuses','juan','tromelin','mascaraignes']

#Indices in the configuration corresponding to the region for plots without projections

xylims={}
xylims['CALEDO60']={}
xylims['CALEDO60']['caledo']=[0,787,0,852]

xylims['eORCA36.L121']={}
xylims['eORCA36.L121']['global']=[0,12959,0,10841]
xylims['eORCA36.L121']['natl']=[6732,10504,6152,8924]
xylims['eORCA36.L121']['satl']=[7812,11052,3436,6152]
xylims['eORCA36.L121']['windian']=[11052,12959,3436,7292]
xylims['eORCA36.L121']['eindian']=[0,1693,3436,7292]
xylims['eORCA36.L121']['npac']=[972,7500,6152,8996]
xylims['eORCA36.L121']['spac']=[2500,7812,3436,6152]
xylims['eORCA36.L121']['med']=[9972,12042,7289,8400]
xylims['eORCA36.L121']['eqpac']=[1972,7500,6152,6152]

# Lat and lon defining the region in a plot with projection


latlon_lims={}
latlon_lims['CALEDO60']={}
latlon_lims['CALEDO60']['caledo']=[0,787,0,852]

latlon_lims['eORCA36.L121']={}
latlon_lims['eORCA36.L121']['global']=[-180,180,-90,90]
latlon_lims['eORCA36.L121']['natl']=[-100,0,0,60]
latlon_lims['eORCA36.L121']['satl']=[-70,20,-60,0]
latlon_lims['eORCA36.L121']['arctic']=[-180,180,60,90]
latlon_lims['eORCA36.L121']['antarctic']=[-180,180,-90,-60]
latlon_lims['eORCA36.L121']['indian']=[20,120,-60,30]
latlon_lims['eORCA36.L121']['npac']=[100,-70,0,60]
latlon_lims['eORCA36.L121']['spac']=[100,-70,-60,0]
latlon_lims['eORCA36.L121']['med']=[-10,50,30,50]
latlon_lims['eORCA36.L121']['npac']=[100,-70,0,0]
latlon_lims['eORCA36.L121']['madagascar']=[30,65,0,-30]
latlon_lims['eORCA36.L121']['bassas']=[35,45,-25,-15]
latlon_lims['eORCA36.L121']['glorieuses']=[40,50,-15,-9]
latlon_lims['eORCA36.L121']['juan']=[40,45,-20,-15]
latlon_lims['eORCA36.L121']['tromelin']=[50,60,-20,-10]
latlon_lims['eORCA36.L121']['mascaraignes']=[50,65,0,-15]

## All the regions we can plot in sections for each configuration
sections_name={'ber':'Bering','fram':'Fram','baf':'Baffin','floba':'Florida-Bahamas','moz':'Mozambique','afraus1':'Africa-Australia1','afraus2':'Africa-Australia2','ausam':'Australia-America','amafr':'America-Africa','cuflo':'Cuba-Florida','ausant':'Australia-Antartica','indo':'Indonesian throughflow','safr':'South Africa','kerg':'Kerguelen','camp':'Campbell','dra':'Drake'}

sections_list={}
sections_list['eORCA36.L121']=['ber','fram','baf','floba','moz','afraus1','afraus2','ausam','amafr','cuflo','ausant','indo','safr','kerg','camp','dra']

sections_deplim={'ber':70,'fram':5000,'baf':2500,'floba':900,'moz':3500,'afraus1':6000,'afraus2':6000,'ausam':6000,'amafr':6000,'cuflo':1200,'ausant':5000,'indo':6000,'safr':6000,'kerg':5000,'camp':6000,'dra':6000}

sections_orientation={'ber':'lat','fram':'lat','baf':'lat','floba':'lat','moz':'lat','afraus1':'lat','afraus2':'lat','ausam':'lat','amafr':'lat','cuflo':'lon','ausant':'lon','indo':'lon','safr':'lon','kerg':'lon','camp':'lon','dra':'lon'}

sections_coords={}
sections_coords['eORCA36.L121']={'ber':[9181,4062,4135],'fram':[10145,9600,9945],'baf':[9955,8331,8812],'floba':[7154,7446,7498],'moz':[5563,11763,11934],'afraus1':[5258,11406,12959],'afraus2':[5258,0,1578],'ausam':[5258,2835,7797],'amafr':[5258,8634,10861],'cuflo':[7435,7003,7106],'ausant':[2725,2732,4696],'indo':[1524,5359,5854],'safr':[11050,2576,4832],'kerg':[12823,2794,4108],'camp':[3504,2386,4300],'dra':[7914,2954,3790]}

# All the variables we can extract and the associated name and filetyp for each simulations

variable_list=['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','MOD','VORT','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','bathy']

compute={}
for var in ['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX']:
    compute[var]=False
for var in ['MOD','VORT']:
    compute[var]=True

compute_filetyp={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    compute_filetyp[simu]={}
    for var in ['MOD','VORT']:
        compute_filetyp[simu][var]=['gridU','gridV']

compute_varname={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    compute_varname[simu]={}
    for var in ['MOD','VORT']:
        compute_varname[simu][var]=['uos','vos']

vars_dim={}
for var in ['SSH','SSU','SSV','SSS','SST','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','MOD','VORT','bathy']:
    vars_dim[var]='2D'
for var in ['T','S','U','V','W']:
    vars_dim[var]='3D'

vars_palette={'SST':cmocean.cm.thermal,'SSS':cmocean.cm.haline,'T':cmocean.cm.thermal,'S':cmocean.cm.haline,'SSH':'tab20b','MLD':cmocean.cm.deep,'MOD':cmocean.cm.ice_r,'VORT':f.home_made_cmap('on2'),'WINDSP':f.home_made_cmap('on3'),'bathy':cmocean.cm.deep} #'MOD':f.home_made_cmap('on3')
for var in ['SSU','SSV','U','V','W','NETDHEATFLX','SWDHEATFLX','LWDHEATFLX']:
    vars_palette[var]=cmocean.cm.balance
for var in ['SICONC','SITHIC']:
    vars_palette[var]=cmocean.cm.ice
for var in ['NETUPWFLX','PRECIP']:
    vars_palette[var]=cmocean.cm.rain

vars_unit = {'SST':'°C','SSS':'PSU','T':'°C','S':'PSU','SSH':'m','MLD':'m','SSU':'m/s','SSV':'m/s','U':'m/s','V':'m/s','W':'m/d','SICONC':'-','SITHIC':'m','MOD':'m/s','VORT':'-','NETDHEATFLX':'W/m2','NETUPWFLX':'kg/m2/s','PRECIP':'kg/m2/s','WINDSP':'m/s','SWDHEATFLX':'W/m2','LWDHEATFLX':'W/m2','bathy':'m'}

vars_longname = {'SST':'sea surface temperature','SSS':'sea surface salinity','T':'temperature','S':'salinity','SSH':'sea surface height','MLD':'mixed layer depth','SSU':'sea surface x-velocity','SSV':'sea surface y-velocity','U':'x-velocity','V':'y-velocity','W':'z-velocity','SICONC':'sea ice concentration','SITHIC':'sea ice thickness','MOD':'module de vitesse de courant de surface','VORT':'vorticite de surface relative','NETDHEATFLX':'Net Downward Heat Flux','NETUPWFLX':'Net Upward Water Flux','PRECIP':'Total precipitation','WINDSP':'wind speed module','SWDHEATFLX':'Shortwave Radiation','LWDHEATFLX':'Longwave Downward Heat Flux over open ocean','bathy':'Bathymetry'}

vars_name={}
vars_name['TRPC12NT0']={'SSH':'zos','SSU':'uos','SSV':'vos'}
vars_name['TRPC12N00']={'SSH':'zos','SSU':'uos','SSV':'vos'}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10']:
    vars_name[simu]={'SSH':'zos','SSU':'uos','SSV':'vos','SSS':'sos','SST':'tos','U':'vozocrtx','V':'vomecrty','W':'vovecrtz','S':'vosaline','T':'votemper','SICONC':'siconc','SITHIC':'sithic','MLD':'somxl010','TAUM':'taum','QSROCE':'qsr_oce','QNSOCE':'qns_oce','PRECIP':'sowapre','WINDSP':'sowinsp','NETDHEATFLX':'sohefldo','SWDHEATFLX':'soshfldo','QNS':'qns','LDHEATFLX':'solhflup','LWDHEATFLX':'solwfldo','SDHEATFLX':'sosbhfup','NETUPWFLX':'sowaflup','DSALTFLX':'sosfldow','DAMPWFLX':'sowafld'}
vars_name['grid']={'bathy':'bathy_metry'}

filetyp={}
filetyp['TRPC12NT0']={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
filetyp['TRPC12N00']={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
filetyp['grid']={'bathy':'domain_noisf_v2_4.2'}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    filetyp[simu]={}
    for var in ['SSH','SSS','SST','T','S','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','MOD','VORT','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX']:
        filetyp[simu][var]='gridT'
    for var in ['SSU','U','SBU','TAUUO']:
        filetyp[simu][var]='gridU'
    for var in ['SSV','V','SBV','TAUVO']:
        filetyp[simu][var]='gridV'
    filetyp[simu]['W']='gridW'
    for var in ['SICONC','SITHIC']:
        filetyp[simu][var]='icemod'

depname={}
for var in ['T','S','MOD','VORT']:
    depname[var]='deptht'
for var in ['U'] :
    depname[var]='depthu'
for var in ['V'] :
    depname[var]='depthv'
for var in ['W'] :
    depname[var]='depthw'

vars_vlims={}
vars_vlims['npole']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['spole']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['global']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,1.5],'VORT':[-1,1],'NETDHEATFLX':[-500,500],'NETUPWFLX':[-0.0005,0.0005],'PRECIP':[0,0.002],'WINDSP':[0,25],'SWDHEATFLX':[-500,500],'LWDHEATFLX':[-500,500]}
vars_vlims['natl']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['satl']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['arctic']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['antarctic']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['windian']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['eindian']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['npac']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['spac']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['med']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['eqpac']={'SSH':[-1,2],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,37],'SST':[20,35],'MLD':[0,100],'MOD':[0,2],'VORT':[-1,1]}
vars_vlims['ber']={'T':[-1.8,-1.6],'S':[31.7,32.6],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['fram']={'T':[-2,4],'S':[30,36],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['baf']={'T':[-2,1],'S':[30,35],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['floba']={'T':[7,27],'S':[35,7],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['moz']={'T':[0,27],'S':[34.9,35.6],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['afraus1']={'T':[0,27],'S':[34.6,36.2],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['afraus2']={'T':[0,27],'S':[34.6,36.2],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['ausam']={'T':[0,27],'S':[34.25,36.5],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['amafr']={'T':[0,27],'S':[33.5,37],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['cuflo']={'T':[5,26],'S':[35,37],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['ausant']={'T':[-2,18],'S':[33,35.6],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['indo']={'T':[0,30],'S':[33.8,35.6],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['safr']={'T':[-2,22],'S':[32,36],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['kerg']={'T':[-3,5],'S':[33.4,35],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['camp']={'T':[-2,13],'S':[33.4,35],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
vars_vlims['dra']={'T':[-2,10],'S':[32.75,35],'U':[-1,1],'V':[-1,1],'W':[-10,10]}
for reg in ['madagascar','bassas','glorieuses','juan','tromelin','mascaraignes']:
    vars_vlims[reg]={'bathy':[0,6000]}

# The time frequency available for a given variable and simulation

frequencies={}
frequencies['TRPC12NT0']={'SSH':'1h','SSU':'1h','SSV':'1h'}
frequencies['TRPC12N00']={'SSH':'1h','SSU':'1h','SSV':'1h'}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    frequencies[simu]={'SSH':'1h','SSU':'1h','SSV':'1h','SSS':'1h','SST':'1h','MLD':'1h','SICONC':'1h','SITHIC':'1h','MOD':'1h','VORT':'1h','U':'12h','V':'12h','S':'12h','T':'12h','W':'12h','NETDHEATFLX':'1h','NETUPWFLX':'1h','PRECIP':'1h','WINDSP':'1h','SWDHEATFLX':'1h','LWDHEATFLX':'1h'}

frequencies_file={}
for simu in ['EXP15-10','EXP13-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10','EXP09']:
    frequencies_file[simu]={}
    for var in ['NETDHEATFLX','NETUPWFLX','PRECIP','WINDSP','SWDHEATFLX','LWDHEATFLX','SSH','SSU','SSV','SSS','SST','MLD','SICONC','SITHIC','MOD','VORT','U','V','S','T','W']:
        frequencies_file[simu][var]='12h'

# The period of time covered by a simulation

sim_date_init={'TRPC12NT0':'2012-01-01','EXP13-10':'2017-01-01 11:00'}
for simu in ['EXP15-10','EXP22a-10','EXP22b-10','EXP22c-10','EXP22d-10','EXP22e-10','EXP22f-10','EXP22g-10','EXP22h-10']:
    sim_date_init[simu]='2012-01-01 11:00'
sim_date_init['EXP09']='2017-01-01 11:00'
sim_date_end={'TRPC12NT0':'2018-12-31','EXP15-10':'2012-02-22 23:00','EXP13-10':'2017-01-03 23:00'}
for simu in ['EXP22a-10','EXP22b-10','EXP22c-10','EXP22f-10','EXP22g-10','EXP22h-10']:
    sim_date_end[simu]='2012-01-01 11:00'
for simu in ['EXP22d-10','EXP22e-10']:
    sim_date_end[simu]='2012-01-01 23:00'

mprocs={}
mprocs['map_noproj']=30
mprocs['map_orthoa']=30
mprocs['map_orthop']=30
mprocs['map_plate']=30
mprocs['map_moll']=30
mprocs['sections']=10
mprocs['time_series']=10
mprocs['hovmuller']=10
