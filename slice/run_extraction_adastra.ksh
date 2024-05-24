#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/slice/scripts

for param in eNATL60-BLB002-SST-1d-2009-2010.py; do
	ln -sf ../params/$param .
#	python launch_dataset_extraction.py -param "${param%.*}"
#	python check_dataset_extraction.py -param "${param%.*}"
	python save_dataset_extraction.py -param "${param%.*}"
done
