#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
FREQ=FREQUENCY
YYYY=YEAR
DD=DAY
MM=MONTH
STYLE=STYLENOM

TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}-S/1d/${REG}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines
DFS=dfs

ulimit -s unlimited

SDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}-S/${FREQ}/${REG}

if [ "$STYLE" -eq "$DFS" ]; then
	for file in $(ls ${SDIR}/${CONFIG}${SREG}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc); do
		fileo=$(basename $file | sed "s/${FREQ}/1d/g")
		if [ ! -f  $fileo ]; then
			echo $fileo
			CDFPATH/cdfmoy -l $file -o $fileo -nc4
			rm ${fileo}2.nc
			fileoo=$(echo $fileo | sed 's/.nc/.nc.nc/g')
			mv  $fileoo $fileo
		fi
	done
else
	for file in $(ls ${SDIR}/${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc); do
		fileo=$(basename $file | sed "s/${FREQ}/1d/g")
		if [ ! -f  $fileo ]; then
			echo $fileo
			CDFPATH/cdfmoy -l $file -o $fileo -nc4
			rm ${fileo}2.nc
			fileoo=$(echo $fileo | sed 's/.nc/.nc.nc/g')
			mv  $fileoo $fileo
		fi
	done

fi





