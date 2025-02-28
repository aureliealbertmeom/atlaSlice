#!/bin/bash

#SBATCH --nodes=3
#SBATCH --ntasks=573
#SBATCH -A hmg2840
#SBATCH -J profile
#SBATCH -e profile.e%j
#SBATCH -o profile.o%j
#SBATCH --time=10:00:00
#SBATCH --constraint=GENOA
#SBATCH --exclusive

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

srun --multi-prog tmp_mpmd_extract_anna_profiles.ksh
