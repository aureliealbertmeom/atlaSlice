#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in aMNA60-BLBT02-1h-3D-buoy-m07-m08.py aGS-LS60-BLBT02-1h-3D-buoy-m08.py; do
	ln -sf ../params/operations/$param .
#	ln -sf ../params/tests/$param .
#	python launch_operation.py -param "${param%.*}"
	python launch_archive.py -param "${param%.*}"
done
