#!/bin/bash
  

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/scripts

for param in eORCA36-L121-EXP15-global-regions-1h-surface-UV.py; do
        ln -sf ../params/$param .
        python send_plots.py -dataset "${param%.*}"
done


