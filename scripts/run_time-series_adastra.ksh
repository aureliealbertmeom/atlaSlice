#!/bin/bash
  
source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/scripts

for param in eORCA36-L121-EXP22all-all-regs-1h-surface-all-plots.py; do
	ln -sf ../params/$param .
	python launch_time-series.py -dataset "${param%.*}"
done

