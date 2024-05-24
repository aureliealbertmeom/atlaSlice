#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
FREQ=FREQUENCY
YYYY=YEAR
MM=MONTH
STYLE=STYLENOM

TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/1d
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines
DFS=dfs

ulimit -s unlimited

SDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}

if [ "${STYLE}" == "${DFS}" ]; then
	for file in $(ls ${SDIR}/${CONFIG}${SREG}_y${YYYY}m${MM}d??.${FREQ}_${VAR}.nc); do
		fileo=$(basename $file | sed "s/${FREQ}/1d/g")
		if [ ! -f  $fileo ]; then
			echo $fileo
			CDFPATH/cdfmoy -l $file -o $fileo -nc4
			rm ${fileo}2.nc
		fi
	done
fi



