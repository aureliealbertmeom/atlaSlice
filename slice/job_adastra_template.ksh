#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=NPROCS
#SBATCH -A hmg2840
#SBATCH -J extract
#SBATCH -e extract.e%j
#SBATCH -o extract.o%j
#SBATCH --time=03:00:00
#SBATCH --constraint=GENOA
#SBATCH --exclusive

NB_NPROC=NPROCS 

srun --multi-prog ./MPMDCONF
