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
STYLE=STYLENOM
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

		fileo=${CONFIG}${SREG}_y${YYYY}m${MM}.${FREQ}_${VAR}m.nc

		if [ ! -f  $fileo ]; then

                        echo $fileo
                        cp $file $fileo

                        MASKF=$(basename $MASKFILE)
			if [ ! -f MASKF ]; then
				ln -sf MASKF .
			fi

                        ncks -A -v MASKNAME MASKF $fileo
                        length=$(ncdump -h $fileo | grep 'time_counter = UNLIMITED' | awk  '{print $6}' | tail -c 4)
                        for t in $(seq 0 `expr $length`); do
                            ncap2 -O -s "VNAME($t,:,:)=VNAME($t,:,:)*MASKNAME(0,:,:)" $fileo $fileo
                        done

                        ncks -O -x -v MASKNAME $fileo $fileo


		fi
	done
fi


