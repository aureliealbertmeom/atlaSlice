#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/slice

for param in SICIL60-BLBT02-1h-TSUVW-archive-m01.py SICIL60-BLBT02-1h-TSUVW-archive-m02.py SICIL60-BLBT02-1h-TSUVW-archive-m07.py SICIL60-BLBT02-1h-TSUVW-archive-m08.py SICIL60-BLBT02-1h-TSUVW-archive-m09.py; do
	ln -sf ../params/$param .
	python save_dataset_extraction.py -param "${param%.*}"
done
