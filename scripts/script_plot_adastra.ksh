#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc
load_conda

conda activate plots

cd SCRIPTDIR

python script_plot.py -mach MACHINE -config CONFIGURATION -simu SIMULATION -var VARIABLE -reg PLOTREGION -loc LOCATION -typ TYPE -freq FREQUENCY -date 'DATE'
