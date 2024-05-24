#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/test

for param in  test-project-wind-one-month.py; do
        python project_sosie.py -param "${param%.*}"
done

