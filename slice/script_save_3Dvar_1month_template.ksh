#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
FREQ=FREQUENCY
YYYY=YEAR
MM=MONTH
INPLACE=YON

TDIR=SCPATH
STDIR=STPATH/${CONFIG}/${CONFIG}-${CASE}-S/${FREQ}/${REG}

if [ ! -d $TDIR ]; then
	echo "Source directory does not exist, aborting operation"
	exit
fi

ulimit -s unlimited

if [ $INPLACE == 'Y' ]; then
	cd $STDIR
	echo "We are in " $STDIR
	if [ ! -f ${STDIR}/TARNAME ]; then
		tar -cvf TARNAME ${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}*.${FREQ}_${VAR}.nc
	else
		echo "be careful, archive already exists, erase it first if you want to replace it"
	fi
else
	mkdir -p $STDIR
	cd $TDIR

	echo "We are in " $TDIR

	if [ ! -f ${STDIR}/TARNAME ]; then
		tar -cvf TARNAME ${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}*.${FREQ}_${VAR}.nc
		dd if=TARNAME of=${STDIR}/TARNAME bs=20M
	else
		echo "be careful, archive already exists, erase it first if you want to replace it"
	fi
fi


