#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc
load_conda

conda activate plots

cd /lus/home/CT1/ige2071/aalbert/git/atlas/scripts

python plots_run.py
