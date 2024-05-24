#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/test

for param in test-one-archive-3Dmonth.py ; do
        python save_dataset_extraction.py -param "${param%.*}"
done

