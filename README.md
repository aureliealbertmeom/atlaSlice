# atlaSlice

## General description

This package regroups 2 main purposes in one library : (1) produce pictures and (2) make extractions from NEMO outputs.

It is designed to work on french supercomputers (adastra, jean-zay and irene) and paralellize the operations with a collection of python and bash scripts.

For instance, if I want to plot annual global SSH for a simulation that ran over 10 years, a script that produces one map of SSH for a given year will be written and will run simultaneously in one job. That way, producing 10 maps of SSH should be as fast as producing one, if we have access to 10 cores of course.

## Organization

The package is organized in 6 subsections

### env
The env section contain the [conda requirements file](env/plots_env.txt) that will install all the needed python librairies with the command ````conda create --name lots --file plots_env.txt```

### params 
The params section contain 3 definition scripts : 
     - a [script](params/template_simulations_dict.py) that gathers all the information about the simulations that we could want to plot or extract, on every machine and every characteristics that define them (period, frequency of outputs, name of variables, indices for regions and sections given a configuration, etc ...) 
     - a [similar script](params/template_plots_dict.py) for the plots parameters (palettes, range of values)
     - a [similar script](params/template_slice_dict.py) for the extraction and computation parameters 

These 3 scripts must be modified by the user to fit his/her needs, then be renamed respectively simulations_dict.py, plots_dict.py and slice_dict.py, these files already exist and contain all the informations gathered for my personnal use 

A user must then define the kind of operation he/she wishes to perform and all the parameters associated in a [param file](params/example_plot_definitions.py) in accordance with what has been defined in the definition scripts.


