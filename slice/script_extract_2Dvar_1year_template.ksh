#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
VARNAME=VNAME
FREQ=FREQUENCY
YYYY=YEAR
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
BRODEAU_eNATL_SPINUP=brodeau_enatl_spinup
MOLINES=molines
JMB=jmb

ulimit -s unlimited

if [ "${STYLE}" == "${JMB}" ]; then
        for file in $(ls ${SDIR}/${CONFIG}${CASE}_${FREQ}_${YYYY}*_${TYP}.nc); do
                day=$(basename $file | awk -F_ '{print $6}' | awk -F- '{print $2}' | awk -F. '{print $1}')
                DD=$(echo "${day: -2}")
                fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done
fi

