#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for param in eORCA36-L121-EXP15-S-archive.py; do
	ln -sf ../params/operations/$param .
	python launch_archive_output.py -param "${param%.*}"
done
