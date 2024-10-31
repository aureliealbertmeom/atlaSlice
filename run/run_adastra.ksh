#!/bin/bash

param=$1

source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/atlas

for param in example_param.py; do
	ln -sf ../params/operations/$param .
	python launch.py -dataset "${param%.*}"
done

for param in example_param.py; do
        rm $param
done

