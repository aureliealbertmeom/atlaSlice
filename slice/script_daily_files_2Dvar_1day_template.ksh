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
BRODEAU_eNATL_SPINUP=brodeau_enatl_spinup
MOLINES=molines
DFS=dfs
JMB=jmb

ulimit -s unlimited

if [ "${STYLE}" == "${DFS}" ]; then
	for file in $(ls ${CONFIG}${SREG}_y${YYYY}m${MM}.${FREQ}_${VAR}.nc); do

		fileo=${CONFIG}${SREG}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc

		if [ ! -f  $fileo ]; then

                        echo $fileo

			NCOPATH/ncks -F -d time_counter,$TI,$TF $file $fileo


		fi
	done
fi

if [ "${STYLE}" == "${BRODEAU_eNATL_SPINUP}" ]; then
        for file in $(ls ${CONFIG}${SREG}-${CASE}_TAG1-TAG2.${FREQ}_${VAR}.nc); do

                fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc

                if [ ! -f  $fileo ]; then

                        echo $fileo

                        NCOPATH/ncks -F -d time_counter,$TI,$TF $file $fileo


                fi
        done
fi

if [ "${STYLE}" == "${JMB}" ]; then
        for file in $(ls SOURCEDIR/MEMBER${CONFIG}${SREG}${CASE}_${FREQ}_TAG1_TAG2_TYP.nc); do

                fileo=MEMBER${CONFIG}${SREG}${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_TYP.nc

                if [ ! -f  $fileo ]; then

                        echo $fileo

                        NCOPATH/ncks -F -d time_counter,$TI,$TF $file $fileo


                fi
        done
fi

