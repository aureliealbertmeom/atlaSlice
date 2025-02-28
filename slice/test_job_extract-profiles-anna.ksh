#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=192
#SBATCH -A hmg2840
#SBATCH -J profile
#SBATCH -e profile.e%j
#SBATCH -o profile.o%j
#SBATCH --time=23:00:00
#SBATCH --constraint=GENOA
#SBATCH --exclusive

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

python extractions-gradients-all-variables-boxes-2024-12-03.py GS 0 20090701
