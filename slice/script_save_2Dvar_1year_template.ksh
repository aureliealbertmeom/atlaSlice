#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
FREQ=FREQUENCY
YYYY=YEAR

TDIR=SCPATH
STDIR=STPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}

mkdir -p $STDIR

cd $TDIR

echo "We are in " $TDIR

ulimit -s unlimited

if [ ! -f ${STDIR}/TARNAME ]; then
	tar -cvf TARNAME ${CONFIG}${SREG}-${CASE}_y${YYYY}*.${FREQ}_${VAR}.nc
	dd if=TARNAME of=${STDIR}/TARNAME bs=20M
else
	echo "be careful, archive already exists, erase it first if you want to replace it"
fi

