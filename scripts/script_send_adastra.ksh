#!/bin/bash

source /lus/home/NAT/gda2307/aalbert/.bashrc

cd PLOTDIR

ssh drakkar@ige-meom-drakkar.u-ga.fr -l drakkar " if [ ! -d DRAKKAR/CONFIGURATION/CONFIGURATION-SIMULATION/REGION/PLOTS ] ; then mkdir -p DRAKKAR/CONFIGURATION/CONFIGURATION-SIMULATION/REGION/PLOTS ; fi "

scp PLOTNAME drakkar@ige-meom-monit.u-ga.fr:~/DRAKKAR/CONFIGURATION/CONFIGURATION-SIMULATION/REGION/PLOTS/.


