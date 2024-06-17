#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/slice/scripts

for param in GULF60-CJM165-daily-degraded-3D-TS.py; do
	ln -sf ../params/$param .
	python launch_dataset_extraction.py -param "${param%.*}"
#	python check_dataset_extraction.py -param "${param%.*}"
i#	python save_dataset_extraction.py -param "${param%.*}"
done
