#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in ANNA60-BLBT02-1h-3D-W.py; do
#for param in ANNA60-BLBT02-mask.py; do
	ln -sf ../params/operations/$param .
	python launch_operation.py -param "${param%.*}"
#	python check_dataset_extraction.py -param "${param%.*}"
done
