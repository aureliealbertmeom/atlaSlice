#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
#conda activate plots

source /lus/work/CT1/hmg2840/aalbert/DEV/conda/atlaslice/bin/activate

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in PORT60degrad4-BLB002X-1h-3D-TSUVW-m05.py; do 
	#PORT60-BLB002X-1h-3D-TSUVW-m05.py; do

	#aMNA60-BLBT02-1h-3D-buoy-m07-m08.py aGS-LS60-BLBT02-1h-3D-buoy-m08.py; do
	ln -sf ../params/operations/$param .
#	ln -sf ../params/tests/$param .
	python launch_operation.py -param "${param%.*}"
#	python launch_archive.py -param "${param%.*}"
done
