#!/bin/bash
  
dataset=$1

source /lus/home/NAT/gda2307/aalbert/.bashrc

load_conda
conda activate plots

python launch_movies.py -dataset "${dataset%.*}"

