import cmocean

# Machines list

machine_list=['adastra','jean-zay','irene']

# Directories on each machine

script_path={}
script_path['adastra']='/lus/home/CT1/ige2071/aalbert/git/atlas'

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
simulation_list['adastra']['eORCA36.L121']=['EXP15-10']

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory['adastra']={}
directory['adastra']['CALEDO60']={}
directory['adastra']['CALEDO60']['TRPC12NT0']='/lus/store/CT1/ige2071/brodeau/TROPICO12/TROPICO12_NST-TRPC12NT0-S'

directory['adastra']['eORCA36.L121']={}
directory['adastra']['eORCA36.L121']['EXP15-10']='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-EXP15-10/eORCA36.L121-EXP15-10-S'

stylenom={}
stylenom['adastra']={}
stylenom['adastra']['CALEDO60']={}
stylenom['adastra']['CALEDO60']['TRPC12NT0']='brodeau_nst'

stylenom['adastra']['eORCA36.L121']={}
stylenom['adastra']['eORCA36.L121']['EXP15-10']='aalbert_gda'

maskfile={}
maskfile['adastra']={}
maskfile['adastra']['EXP15-10']='/lus/work/NAT/gda2307/aalbert/eORCA36.L121/eORCA36.L121-I/eORCA36.L121_mesh_mask_noisf_v2_4.2.nc'

# All the regions we can plot in 2D maps for each configuration

regions_list={}
regions_list['CALEDO60']=['caledo']

regions_list['eORCA36.L121']=['global','natl','satl','arctic','antarctic','indian','windian','eindian','npac','spac','med']

#Indices in the configuration corresponding to the region for plots without projections

xylims={}
xylims['CALEDO60']={}
xylims['CALEDO60']['caledo']=[0,787,0,852]

xylims['eORCA36.L121']={}
xylims['eORCA36.L121']['global']=[0,12959,0,10841]
xylims['eORCA36.L121']['natl']=[6732,10198,6152,8843]
xylims['eORCA36.L121']['satl']=[7812,11052,3436,6152]
xylims['eORCA36.L121']['windian']=[11052,12959,3436,7292]
xylims['eORCA36.L121']['eindian']=[0,1693,3436,7292]
xylims['eORCA36.L121']['npac']=[972,7977,6152,8996]
xylims['eORCA36.L121']['spac']=[972,7812,3436,6152]
xylims['eORCA36.L121']['med']=[10692,12042,7289,8834]

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
latlon_lims['eORCA36.L121']['med']=[10,50,30,50]

## All the regions we can plot in sections for each configuration
sections_name={'ber':'Bering','fram':'Fram','baf':'Baffin','floba':'Florida-Bahamas','moz':'Mozambique','afraus1':'Africa-Australia1','afraus2':'Africa-Australia2','ausam':'Australia-America','amafr':'America-Africa','cuflo':'Cuba-Florida','ausant':'Australia-Antartica','indo':'Indonesian throughflow','safr':'South Africa','kerg':'Kerguelen','camp':'Campbell','dra':'Drake'}

sections_list={}
sections_list['eORCA36.L121']=['ber','fram','baf','floba','moz','afraus1','afraus2','ausam','amafr','cuflo','ausant','indo','safr','kerg','camp','dra']

sections_deplim={'ber':70,'fram':5000,'baf':2500,'floba':900,'moz':3500,'afraus1':6000,'afraus2':6000,'ausam':6000,'amafr':6000,'cuflo':1200,'ausant':5000,'indo':6000,'safr':6000,'kerg':5000,'camp':6000,'dra':6000}

sections_orientation={'ber':'lat','fram':'lat','baf':'lat','floba':'lat','moz':'lat','afraus1':'lat','afraus2':'lat','ausam':'lat','amafr':'lat','cuflo':'lon','ausant':'lon','indo':'lon','safr':'lon','kerg':'lon','camp':'lon','dra':'lon'}

sections_coords={}
sections_coords['eORCA36.L121']={'ber':[9181,4062,4135],'fram':[10145,9600,9945],'baf':[9955,8331,8812],'floba':[7154,7446,7498],'moz':[5563,11763,11934],'afraus1':[5258,11406,12959],'afraus2':[5258,0,1578],'ausam':[5258,2835,7797],'amafr':[5258,8634,10861],'cuflo':[7435,7003,7106],'ausant':[2725,2732,4696],'indo':[1524,5359,5854],'safr':[11050,2576,4832],'kerg':[12823,2794,4108],'camp':[3504,2386,4300],'dra':[7914,2954,3790]}

# All the variables we can extract and the associated name and filetyp for each simulations

variable_list=['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC']

vars_dim={'SSH':'2D','SSU':'2D','SSV':'2D','SST':'2D','SSS':'2D','T':'3D','S':'3D','U':'3D','V':'3D','W':'3D','TAUM':'2D','TAUBOT':'2D','QTOCE':'2D','QSROCE':'2D','QSBOCE':'2D','QNSOCE':'2D','QLWOCE':'2D','QLAOCE':'2D','PRECIP':'2D','EVAPOCE':'2D','EMPMR':'2D','WINDSP':'2D','RHOAIR':'2D','MLD':'2D','SBU':'2D','TAUUO':'2D','SBV':'2D','TAUVO':'2D','SICONC':'2D','SITHIC':'2D','MLD':'2D'}

vars_palette={'SST':cmocean.cm.thermal,'SSS':cmocean.cm.haline,'SSH':'tab20c','MLD':cmocean.cm.deep ,'SSU':cmocean.cm.balance,'SSV':cmocean.cm.balance,'SICONC':cmocean.cm.ice,'SITHIC':cmocean.cm.ice }

vars_unit = {'SST':'°C','SSS':'PSU','SSH':'m','MLD':'m','SSU':'m/s','SSV':'m/s','SICONC':'-','SITHIC':'m'}

vars_longname = {'SST':'sea surface temperature','SSS':'sea surface salinity','SSH':'sea surface height','MLD':'mixed layer depth','SSU':'sea surface x-velocity','SSV':'sea surface y-velocity','SICONC':'sea ice concentration','SITHIC':'sea ice thickness'}

vars_name={}
vars_name['TRPC12NT0']={'SSH':'zos','SSU':'uos','SSV':'vos'}
vars_name['TRPC12N00']={'SSH':'zos','SSU':'uos','SSV':'vos'}
vars_name['EXP15-10']={'SSH':'zos','SSU':'uos','SSV':'vos','SSS':'sos','SST':'tos','SICONC':'siconc','SITHIC':'sithic','MLD':'somxl010'}

filetyp={}
filetyp['TRPC12NT0']={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
filetyp['TRPC12N00']={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
filetyp['EXP15-10']={'SSH':'gridT','SSS':'gridT','SST':'gridT','SSU':'gridU','SSV':'gridV','SICONC':'icemod','SITHIC':'icemod','MLD':'gridT'}

vars_vlims={}
vars_vlims['global']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['natl']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['satl']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['arctic']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['antarctic']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['windian']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['eindian']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['npac']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['spac']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}
vars_vlims['med']={'SSH':[-2,5],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10]}

# The time frequency available for a given variable and simulation

frequencies={}
frequencies['TRPC12NT0']={'SSH':'1h','SSU':'1h','SSV':'1h'}
frequencies['TRPC12N00']={'SSH':'1h','SSU':'1h','SSV':'1h'}
frequencies['EXP15-10']={'SSH':'1h','SSU':'1h','SSV':'1h','SSS':'1h','SST':'1h','MLD':'1h','SICONC':'1h','SITHIC':'1h'}

frequencies_file={}
frequencies_file['EXP15-10']={'SSH':'12h','SSU':'12h','SSV':'12h','SSS':'12h','SST':'12h','MLD':'12h','SICONC':'12h','SITHIC':'12h'}

# The period of time covered by a simulation

sim_date_init={'TRPC12NT0':'2012-01-01','EXP15-10':'2012-01-01 11:00'}
sim_date_end={'TRPC12NT0':'2018-12-31','EXP15-10':'2012-02-22 23:00'}

