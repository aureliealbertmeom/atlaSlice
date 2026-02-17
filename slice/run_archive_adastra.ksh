#!/bin/bash

source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda

source /lus/work/CT1/hmg2840/aalbert/DEV/conda/atlaslice/bin/activate

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in eNATL60-SIDRA.py ; do
	ln -sf ../params/operations/$param .
	python launch_archive.py -param "${param%.*}"
done
