#! /usr/bin/env python

"""
This is an example plots definition
=====================================
This is where the user defines what he/she wants to plot or extract/compute and where
A beginner user may look at the simulations_dict.py and plots_dict.py or slice_dict.py files 
to see what can be done and where
An advanced user modifies the dict files to match their needs
Be careful not to put a . in the name of this file
Written in 2024-02-07 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""

# Machine where the plots/extractions are performed and hopefully the raw data are stored
# It can be only one in adastra, jean-zay or irene
machine='adastra'

# Name of the configuration
# It must be one of the configuration outputs stored on the above machine
configuration='eORCA36.L121'

# Simulation, experiment or run
# It must be one of the simulations for the above configuration stored on the above machine
simulations=['EXP15-10']

# Variables considered for plots/extractions
# It must be in the list of acceptable variables
variables=['SSH','SSU','SSV','SSS','SST','MLD','SICONC','SITHIC']

# Type of operation 
# It can be a plot : either a map, a section or a time-serie
# or an operation like : extract, degrad10 or apply_mask
operation=['noproj_map']

# Name of the regions considered for extraction or plots
# It must have been defined for the selected configuration
regions=['UKFR']

# Extra parameters of the plot
# This specifies the depth for maps, the coordinates for sections or time-series
extra_params=['surf']

# Frequency of the plots or outputs
# It must be compatible for the simulation and variable
frequency='1h'

# Perform the archive or not
archive='N'

# Period of the extraction
# Must be in the format yyyy-mm-dd
date_init='2012-02-22 23:00'
date_end='2012-02-22 23:00'

