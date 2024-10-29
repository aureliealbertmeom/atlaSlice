# atlaSlice

This package regroups 2 main purposes in one library : produce pictures and make extractions from NEMO outputs 
It is designed to work on french supercomputers (adastra, jean-zay and irene) and paraellize the operations with a collection of python and bash scripts.

For instance, if I want to plot annual global SSH for a simulation, a script that produces one map of SSH for a given year will be written and will run simultaneously in one job. That way, producing 10 maps of SSH should be as fast as producing one, if we have access to 10 cores of course.


A user must first define the kind of operation he/she wishes to perform and all the parameters associated in a [param file](params/example_plot_definitions.py)
