#!/bin/bash

#MSUB -r slice               # Job name
#MSUB -N 1                # Number of tasks to use
#MSUB -n 2                # Number of tasks to use
#MSUB -T 21600               # Elapsed time limit in seconds
#MSUB -o slice.o%I           # Standard output. %I is the job id
#MSUB -e slice.e%I           # Error output. %I is the job id
#MSUB -q rome               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -x
#MSUB -m work,scratch


NB_NPROC=2 

source ~/.bashrc
load_intel

srun --multi-prog ./tmp_mpmd2_compute_bottom_pressure_irene_ORCA025.L75_OCCITENS.001_global_BOTPRES_1m_1980-01-01_1980-12-31.ksh
