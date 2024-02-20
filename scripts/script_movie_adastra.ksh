#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc
load_conda

conda activate plots

cd PLOTDIR

filed=PLOT_DEBUT
filem=PLOT_MILIEU
filee=.png

fileo=MOVIENAME


ffmpeg -f image2 -pattern_type glob -r 25 -i "${filed}*${filem}*${filee}" -crf 20 -refs 16 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"  $fileo

ssh drakkar@ige-meom-drakkar.u-ga.fr -l drakkar " if [ ! -d DRAKKAR/CONFIGURATION/CONFIGURATION-SIMULATION/REGION ] ; then mkdir DRAKKAR/CONFIGURATION/CONFIGURATION-SIMULATION/REGION ; fi "

scp $fileo drakkar@ige-meom-monit.u-ga.fr:~/DRAKKAR/CONFIGURATION/CONFIGURATION-SIMULATION/REGION/.

rm $fileo

