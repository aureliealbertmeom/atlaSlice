#!/bin/bash
  
source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/atlas

#./clean.ksh

for param in eNATL60-bathy-ANNA.py; do
	ln -sf ../params/operations/$param .
	python launch_plots.py -dataset "${param%.*}"
done

