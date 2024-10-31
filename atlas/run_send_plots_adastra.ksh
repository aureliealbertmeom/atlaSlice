#!/bin/bash
  
source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/scripts

#./clean.ksh
#for param in eORCA36-L121-EXP15-all-regs-1h-surface-all-time-series.py; do
#for param in eORCA36-L121-EXP15-eqpac-1h-surface-all-hovmuller.py; do
#for param in eORCA36-L121-EXP13-global-1h-surface-fluxes-all-plots.py; do
#for param in test-one-map.py; do
for param in eORCA36-L121-EXP15-global-ortho-1h-surface-MOD.py; do
	ln -sf ../params/$param .
	python send_plots.py -dataset "${param%.*}"
done

