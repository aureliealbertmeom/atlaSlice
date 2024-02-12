#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=NPROCS
#SBATCH -A hmg2840
#SBATCH -J plot
#SBATCH -e plot.e%j
#SBATCH -o plot.o%j
#SBATCH --time=6:00:00
#SBATCH --constraint=HPDA
#SBATCH --exclusive

NB_NPROC=NPROCS

srun --multi-prog ./MPMDCONF
