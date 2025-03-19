#!/bin/bash
source /lus/home/NAT/gda2307/aalbert/.bashrc
load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

for d in $(seq 1 31); do 
	dd=$(printf "%02d" $d);  python extractions-gradients-all-variables-boxes-2024-12-03.py BOXNAME BOXNUMBER  200907$dd
done
