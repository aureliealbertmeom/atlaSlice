#! /usr/bin/env python

"""
This is an example plots definition
=====================================
This is where the user defines what he/she wants to plot and where
A beginner user may look at the simulations_dict.py and plots_dict.py files to see what can be done and where
An advanced user modifies simulations_dict.py and plots_dict.py files to match their needs
Be careful not to put a . in the name of this file
Written in 2024-02-07 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""

# Machine where the plots are performed and hopefully the raw data are stored
# It can be only one above adastra, jean-zay, irene
machine='adastra'

# Name of the configuration
# It must be one of the configuration outputs stored on the above machine
configuration='eORCA36.L121'

# Simulation, experiment or run
# It must be one of the simulations for the above configuration stored on the above machine
simulations=['EXP15-10']

# Variables considered for plots
# It must be in the list of acceptable variables
variables=['SSH','SSU','SSV','SSS','SST','MLD','SICONC','SITHIC']

# Type of plots 
# It must be either a map, a section or a time-serie
plot_types=['noproj_map']

# Parameters of the plot
# This specifies the depth for maps, the coordinates for sections or time-series
plot_params=['surf']

# Region of the plot
# This specifies the region for maps
#plot_regions=['global','natl','satl','arctic','antarctic','indian','npac','spac','med']
plot_regions=['global']

# Frequency of the plots
# It must be compatible for the simulation and variable
frequency='1h'

# Period of the extraction
# Must be in the format yyyy-mm-dd
date_init='2012-02-22 23:00'
date_end='2012-02-22 23:00'

