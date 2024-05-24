#!/bin/bash

cd /lus/scratch/CT1/hmg2840/aalbert/TMPPLOTS/eORCA36.L121/eORCA36.L121-EXP15-10

ssh drakkar@ige-meom-drakkar.u-ga.fr -l drakkar " if [ ! -d DRAKKAR/eORCA36.L121/eORCA36.L121-EXP15-10/HOVMULLER/eqpac ] ; then mkdir -p DRAKKAR/eORCA36.L121/eORCA36.L121-EXP15-10/HOVMULLER/eqpac ; fi "

scp eORCA36.L121-EXP15-10_hovmuller_surf_eqpac_y2012m01d01h11-y2012m02d22h23.1h_SST.png drakkar@ige-meom-monit.u-ga.fr:~/DRAKKAR/eORCA36.L121/eORCA36.L121-EXP15-10/HOVMULLER/eqpac/.
