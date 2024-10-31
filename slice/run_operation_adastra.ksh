#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in SICILe60-BLBT02-1h-TS-JulyAugust2009.py; do
	ln -sf ../params/$param .
#	python launch_archive.py -param "${param%.*}" #if run with archive='F' print the number of files produced by the operation
	python launch_operation.py -param "${param%.*}"
done
