#!/bin/bash

#OAR -n slice
#OAR -l /nodes=1/core=1,walltime=23:00:00
#OAR --stdout slice.out
#OAR --stderr slice.err
#OAR --project pr-data-ocean

source /home/alberta/.bashrc

cd /bettik/alberta/git/atlaSlice/slice

micromamba activate atlaslice

python test_script_prof_flux_filt_inboxes_dahu.py
