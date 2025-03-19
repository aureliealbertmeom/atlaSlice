# atlaSlice

## General description

This package regroups 2 main purposes in one library : (1) produce pictures and (2) make extractions from NEMO outputs.

It is designed to work on french supercomputers (adastra, jean-zay and irene) and paralellize the operations with a collection of python and bash scripts.

For instance, if I want to plot annual global SSH for a simulation that ran over 10 years, a script that produces one map of SSH for a given year will be written and will run simultaneously in one job. That way, producing 10 maps of SSH should be as fast as producing one, if we have access to 10 cores of course.

## Organization

The package is organized in 7 subsections

### env
The env section contain the [conda requirements file](env/plots_env.txt) that will install all the needed python librairies with the command ```conda create --name plots --file plots_env.txt```

### params 
The params section contain 3 definition scripts : 

  - a [script](params/template_simulations_dict.py) that gathers all the information about the simulations that we could want to plot or extract, on every machine and every characteristics that define them (period, frequency of outputs, name of variables, indices for regions and sections given a configuration, etc ...) 
  - a [similar script](params/template_plots_dict.py) for the plots parameters (palettes, range of values)
  - a [similar script](params/template_slice_dict.py) for the extraction and computation parameters 

These 3 scripts must be modified by the user to fit his/her needs, then be renamed respectively simulations_dict.py, plots_dict.py and slice_dict.py, these files already exist and contain all the informations gathered for my personnal use 

A user must then define the kind of operation he/she wishes to perform and all the parameters associated in a [param file](params/operation/example_param.py) in accordance with what has been defined in the definition scripts.

### run
This is where the launching and execution of the scripts will happen.

A user must add the parameters file name defined in the params/operation section in the run script associated to the machine he/she is on : [run_adastra.ksh](run/run_adastra.ksh) for instance.

Several operations can be added and will be performed in a row


## Add new scripts

### In slice

To add a new operation to be done on output files you must :

 - create a script for the operation you want to perform, for instance script_compute_buoyancy_3Dvar_1day_template.ksh will compute buoyancy from 3D temperature and salinity
 - modify the launch_operation.py script to include the option for the new operation buoy and the creation of the scripts from script_compute_buoyancy_3Dvar_1day_template in the function set_up_script_1simulationu_1region_1var_nomask (and in set_up_script_1simulationu_1region_1var_mask if the operation can be done on mask files)
 - specify the option of the operation : compute_buoyancy only work with variable T and after an extraction
 - modify slice_dict.py at least for the number of parallelized operation youcan do on one node, if some new parameters are needed make sure to complete the simulations_dict.py or slice_dict.py files
 - make a test param file in params/tests that will try to execute the operation for one simulation, one variable, one date etc ...
 - also modify launch_archive.py script so that the outputs could be archived
