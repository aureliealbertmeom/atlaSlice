#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=NPROCS
#SBATCH --partition=prepost
#SBATCH -A cli@cpu
#SBATCH -J extract
#SBATCH -e extract.e%j
#SBATCH -o extract.o%j
#SBATCH --time=06:00:00
#SBATCH --exclusive

NB_NPROC=NPROCS 

srun --multi-prog ./MPMDCONF
