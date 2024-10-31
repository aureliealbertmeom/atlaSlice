#!/bin/bash
  
source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/atlas

#./clean.ksh

for param in test-zyplot.py; do
	ln -sf ../params/$param .
	python launch_plots.py -dataset "${param%.*}"
done

