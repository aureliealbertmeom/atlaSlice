#!/bin/bash

source /linkhome/rech/genige01/rote001/.bashrc
module unload anaconda-py3

module load python/3.10.4
cd /lustre/fswork/projects/rech/cli/rote001/DEV/git/atlaSlice/slice

#for param in ENS04-1d-extract-SSH-30members.py; do 
for param in ENS04-1d-SSH-30members.py; do 
	ln -sf ../params/operations/$param .
	python launch_operation.py -param "${param%.*}"
done
