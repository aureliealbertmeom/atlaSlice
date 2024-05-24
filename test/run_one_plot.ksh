#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/test

#for param in test-hovmuller.py ; do
#for param in test-time-serie.py ; do
#for param in test-npole.py ; do
#for param in test-one-map.py ; do
for param in test-one-map-proj-grid.py ; do
	ln -sf ../params/$param .
        python launch_plots.py -dataset "${param%.*}"
done

