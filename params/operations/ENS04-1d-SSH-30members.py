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
machine='jean-zay'

# Name of the configuration
# It must be one of the configuration outputs stored on the above machine
configuration='ENS'

# Name of the simulation, experiment or run
# It must be one of the simulations for the above configuration stored on the above machine
simulations=['04']

# If ensemble simulation, name of the members
# Leave empty '' if not an ensemble simulation
members=['004']

# Name of the regions considered for extraction
# It must have been defined for the selected configuration
regions=['MED']

# Name of the variables considered for extraction
# It must be in the list of acceptable variables
variables=['SSH']

# Frequency of the output
# It must be compatible for the simulation and variable
frequency='1d'

# Extra operation after extraction of raw outputs
operation='daily_files' # daily_files then extract

# Perform the archive or not
archive='N'
# Wether data is already sitting on the store

# Job
job='N'

# Period of the extraction
# Must be in the format yyyy-mm-dd
date_init='1979-06-27'
#date_init='1980-01-01'
#date_end='1979-06-30'
date_end='2020-12-31'


