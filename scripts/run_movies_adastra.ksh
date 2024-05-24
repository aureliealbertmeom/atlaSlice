#!/bin/bash
  

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/scripts

./clean.ksh

#for param in eORCA36-L121-EXP22all-poles-1h-surface-all-plots.py; do
#for param in eORCA36-L121-EXP13-global-1h-surface-fluxes-all-plots.py; do
#for param in eORCA36-L121-EXP15-global-1h-surface-fluxes-all-plots.py; do
for param in eORCA36-L121-EXP15-poles-1h-surface-all-plots.py; do
	if [ ! -f $param ]; then
		ln -sf ../params/$param .
	fi
        python launch_movies.py -dataset "${param%.*}"
done

