#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/slice

for param in DFS5-NATL60-3h-u10-v10-y2009m07-y2010m06.py; do
	ln -sf ../params/$param .
	python project_sosie.py -param "${param%.*}"
done
