#!/bin/bash

source /lus/home/CT1/hmg2840/aalbert/.bashrc

load_conda

source /lus/work/CT1/hmg2840/aalbert/DEV/conda/atlaslice/bin/activate

cd /lus/home/CT1/hmg2840/aalbert/git/atlaSlice/slice

python launch_script_irene_compute_bottom_pressure.py
