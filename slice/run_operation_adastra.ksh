#!/bin/bash

source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda

source /lus/work/CT1/hmg2840/aalbert/DEV/conda/atlaslice/bin/activate

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

#for param in PORT60-BLB002X-1d-3D-TSUVW-m05.py; do 
for param in ANNA60-BLBT02-1h-prof-flux-filt-inboxes-buoyancy.py; do 
#for param in ANNA60-BLBT02-1h-3D-W.py; do 
	ln -sf ../params/operations/$param .
#	ln -sf ../params/tests/$param .
	python launch_operation.py -param "${param%.*}"
#	python launch_archive.py -param "${param%.*}"
done
