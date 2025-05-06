#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
VAR=VARIABLE
FREQ=FREQUENCY
YYYY=YEAR
MM=MONTH
DD=DAY
INPLACE=YON
STYLE=STYLENOM

TDIR=/lus/work/NAT/gda2307/aalbert/${CONFIG}/${CONFIG}-${CASE}/${CONFIG}-${CASE}-S
STDIR=/lus/work/CT1/hmg2840/aalbert/${CONFIG}/${CONFIG}-${CASE}/${CONFIG}-${CASE}-S

if [ ! -d $TDIR ]; then
	echo "Source directory does not exist, aborting operation"
	exit
fi

ulimit -s unlimited

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines
GDALBERT=aalbert_gda

if [ "${STYLE}" == "${GDALBERT}" ]; then

	mkdir -p $STDIR
	cd $TDIR

	echo "We are in " $TDIR

	if [ ! -f ${STDIR}/TARNAME ]; then
		tar -cvf TARNAME */${CONFIG}*_${FREQ}_*${VAR}*${YYYY}${MM}${DD}*.nc
		mv TARNAME ${STDIR}/TARNAME
	else
		echo "be careful, archive already exists, erase it first if you want to replace it"
	fi
fi


