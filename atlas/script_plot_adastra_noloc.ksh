#!/bin/bash

source /lus/home/CT1/hmg2840/aalbert/.bashrc
load_conda

conda activate plots

cd SCRIPTDIR

python script_plot.py -mach MACHINE -config CONFIGURATION -simu SIMULATION -var VARIABLE -reg PLOTREGION -typ TYPE -freq FREQUENCY -date 'DATE'
