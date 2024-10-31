#! /usr/bin/env python

"""
This is an example dataset definition
=====================================
This is where the user defines what he/she wants to extract and where
A beginner user may look at the params.py file to see what is available and where
An advanced user modifies params.py file to match their needs
Written in 2024-01-19 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""

# Machine where the extration is done and hopefully the raw data are stored
# It can be only one above adastra, jean-zay, irene
machine='adastra'

# Name of the configuration
# It must be one of the configuration outputs stored on the above machine
configuration='eNATL60'

# Name of the simulation, experiment or run
# It must be one of the simulations for the above configuration stored on the above machine
simulations=['BLB001'] # BLB001, then BLB002 and BLB002X

# Name of the regions considered for extraction
# It must have been defined for the selected configuration
regions=['CARA']

# Name of the variables considered for extraction
# It must be in the list of acceptable variables
variables=['SSH']

# Frequency of the output
# It must be compatible for the simulation and variable
frequency='1h'

# Extra operation after extraction of raw outputs
operation='degrad10' # degrad10 then degrad10

# Perform the archive or not
archive='N'
# Wether data is already sitting on the store

# Period of the extraction
# Must be in the format yyyy-mm-dd
date_init='2009-01-01' # BLB001 : 2009-03-17, BLB002: 2009-06-30, BLB002X: 2009-11-17
date_end='2009-06-30' # BLB001 : 2009-06-29, BLB002: 2009-11-16, BLB002X:  2010-07-31


