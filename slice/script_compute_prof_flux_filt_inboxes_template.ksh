#!/bin/bash

MAC=MACHINE
CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
VAR=VARIABLE
FREQ=FREQUENCY
DATE=YYYYMMDD

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda

source /lus/work/CT1/hmg2840/aalbert/DEV/conda/atlaslice/bin/activate

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

python script_prof_flux_filt_inboxes.py -mach $MAC -config $CONFIG -simu $CASE -var $VAR -reg $REG -freq $FREQ -date $DATE
