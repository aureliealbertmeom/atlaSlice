#!/bin/bash
  

source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/atlas

./clean.ksh

#for param in eORCA36-L121-EXP22all-poles-1h-surface-all-plots.py; do
#for param in eORCA36-L121-EXP13-global-1h-surface-fluxes-all-plots.py; do
#for param in eORCA36-L121-EXP15-global-1h-surface-fluxes-all-plots.py; do
for param in test-zyplot.py; do
	if [ ! -f $param ]; then
		ln -sf ../params/$param .
	fi
        python launch_movies.py -dataset "${param%.*}"
done

