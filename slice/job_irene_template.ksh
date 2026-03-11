#!/bin/bash

#MSUB -r slice               # Job name
#MSUB -N NPROCS                # Number of tasks to use
#MSUB -n 1                # Number of tasks to use
#MSUB -T 21600               # Elapsed time limit in seconds
#MSUB -o slice.o%I           # Standard output. %I is the job id
#MSUB -e slice.e%I           # Error output. %I is the job id
#MSUB -q rome               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -x
#MSUB -m work,scratch


NB_NPROC=NPROCS 

source ~/.bashrc
load_intel

srun --multi-prog ./MPMDCONF
