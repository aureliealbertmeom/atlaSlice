#!/bin/bash

source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in SICILe60-BLB002-1h-TSUVW-JulyAugust2009.py; do
	ln -sf ../params/$param .
	python test_operation.py -param "${param%.*}"
done
