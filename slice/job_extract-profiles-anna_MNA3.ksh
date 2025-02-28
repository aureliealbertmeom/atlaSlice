#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH -A hmg2840
#SBATCH -J profile
#SBATCH -e profile.e%j
#SBATCH -o profile.o%j
#SBATCH --time=10:00:00
#SBATCH --constraint=HPDA
#SBATCH --exclusive

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

srun --multi-prog tmp_mpmd3_extract_anna_profiles_MNA.ksh
