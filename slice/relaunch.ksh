#!/bin/bash

k=6 # number of times to relaunch the job

job=tmp_job_prof_flux_filt_inboxes_adastra_eNATL60_BLBT02_aMNA_buoyancy_1h_2009-09-01_2009-09-30.ksh

for job in ${list[*]}; do

	jobid=$(sbatch $job | awk '{print $NF}')

	kt=0
	while [ $kt -lt $k ]; do
		jobid=$(sbatch --dependency=afterany:$jobid $job | awk '{print $NF}')
		kt=$(( $kt + 1 ))
	done

done

