#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
VARNAME=VNAME
FREQ=FREQUENCY
YYYY=YEAR
MM=MONTH
DD=DAY
STYLE=STYLENOM
TI=INDTI
TF=INDTF
TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines
DFS=dfs
ulimit -s unlimited

if [ "${STYLE}" == "${DFS}" ]; then
	for file in $(ls ${CONFIG}${SREG}_y${YYYY}m${MM}.${FREQ}_${VAR}.nc); do

		fileo=${CONFIG}${SREG}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc

		if [ ! -f  $fileo ]; then

                        echo $fileo

			ncks -F -d time_counter,$TI,$TF $file $fileo


		fi
	done
fi


