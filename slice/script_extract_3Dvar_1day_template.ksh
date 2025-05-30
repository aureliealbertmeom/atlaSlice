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
TYP=FILETYP
SDIR=SOURCEDIR
STYLE=STYLENOM
X1=XX1
X2=XX2
Y1=YY1
Y2=YY2

TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}-S/${FREQ}/${REG}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines

ulimit -s unlimited

if [ "${STYLE}" == "${BRODEAU_NST}" ]; then
	for file in $(ls ${SDIR}/*/NST/${CASE}-${CONFIG}_${FREQ}_${YYYY}${MM}${DD}_${YYYY}${MM}${DD}_${TYP}.nc4); do
		fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc
		if [ ! -f  $fileo ]; then
			echo $fileo
			NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
		fi
	done
fi

if [ "${STYLE}" == "${BRODEAU_eNATL}" ]; then
        for file in $(ls ${SDIR}/${CONFIG}-${CASE}*-S/*/${CONFIG}-${CASE}*_${FREQ}_*_${TYP}_${YYYY}${MM}${DD}-${YYYY}${MM}${DD}.nc); do
                fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done
fi

if [ "${STYLE}" == "${MOLINES}" ]; then
        for file in $(ls ${SDIR}/${FREQ}/${YYYY}/${CONFIG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${TYP}.nc); do
                fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done
fi
