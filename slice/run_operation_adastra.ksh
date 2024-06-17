#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/slice

for param in GULF60-CJM165-daily-degraded-3D-TS.py; do
	ln -sf ../params/$param .
	python launch_archive.py -param "${param%.*}" #if run with archive='F' print the number of files produced by the operation
#	python launch_operation.py -param "${param%.*}"
done
