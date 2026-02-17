#! /usr/bin/env python

"""
This is an example plots definition
=====================================
This is where the user defines what he/she wants to plot and where
A beginner user may look at the params.py file to see what can be done and where
An advanced user modifies params.py file to match their needs
Be careful not to put a . in the name of this file
Written in 2024-02-07 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""

# Machine where the plots are performed and hopefully the raw data are stored
# It can be only one above adastra, jean-zay, irene
machine='adastra'

# Name of the configuration
# It must be one of the configuration outputs stored on the above machine
configuration='eNATL60'

# Simulation, experiment or run
# It must be one of the simulations for the above configuration stored on the above machine
simulations=['']

# Variables considered for plots
# It must be in the list of acceptable variables
variables=['mask']

# Region of the plot
# This specifies the region for maps
regions=['FAROE','ICEFAR']

# Frequency of the plots
# It must be compatible for the simulation and variable
frequency=''

# Extra operation after extraction of raw outputs
operation='extract' # extract then daily_mean

# Perform the archive or not
archive='Y'
job='N'

# Period of the extraction
# Must be in the format yyyy-mm-dd
date_init=''
date_end=''

