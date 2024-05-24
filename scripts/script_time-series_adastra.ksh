#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc
load_conda

conda activate plots

cd SCRIPTDIR/scripts

python script_time-series.py -mach MACHINE -config CONFIGURATION -simu SIMULATION -var VARIABLE -reg PLOTREGION -loc LOCATION -typ TYPE -freq FREQUENCY -date_init 'DATEI' -date_end 'DATEE'
