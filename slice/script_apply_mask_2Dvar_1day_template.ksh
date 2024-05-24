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
TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}

TMPDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}/tmp_${VAR}_${YYYY}_${MM}_${DD}

mkdir -p $TMPDIR
cd $TMPDIR

echo "We are in " $TMPDIR

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines
DFS=dfs
ulimit -s unlimited

if [ "${STYLE}" == "${DFS}" ]; then
	for file in $(ls ${TDIR}/${CONFIG}${SREG}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc); do

		fileo=${CONFIG}${SREG}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}m.nc

		if [ ! -f  ${TDIR}/$fileo ]; then

                        echo $fileo
                        cp $file $fileo

                        MASKF=$(basename MASKFILE)
			cp ../$MASKF .

                        ncks -A -v MASKNAME $MASKF $fileo
                        length=$(ncdump -h $fileo | grep 'time_counter = UNLIMITED' | awk  '{print $6}' | awk -F '(' '{print $2}')
                        for t in $(seq 0 `expr $length - 1`); do
                            ncap2 -O -s "VNAME($t,:,:)=VNAME($t,:,:)*MASKNAME(0,:,:)" $fileo $fileo
                        done

                        ncks -O -x -v MASKNAME $fileo $fileo


		fi

		cp $fileo ${TDIR}/.
	done
fi


