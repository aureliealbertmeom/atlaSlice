#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH -A hmg2840
#SBATCH -J profiles
#SBATCH -e profiles.e%j
#SBATCH -o profiles.o%j
#SBATCH --time=23:00:00
#SBATCH --constraint=HPDA
#SBATCH --exclusive

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

./tmp_make_extract_anna_profiles_LS.ksh
