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

if [ "${STYLE}" == "${BRODEAU_NST}" ]; then
	for file in $(ls ${SDIR}/*/NST/${CASE}-${CONFIG}_${FREQ}_${YYYY}${MM}??_${YYYY}${MM}??_${TYP}.nc4); do
		day1=$(basename $file | awk -F_ '{print $3}')
		DD1=$(echo "${day1: -2}")
		day2=$(basename $file | awk -F_ '{print $4}')
                DD2=$(echo "${day2: -2}")
		fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD1}-d${DD2}.${FREQ}_${VAR}.nc
		if [ ! -f  $fileo ]; then
			echo $fileo
			NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
		fi
	done
fi

if [ "${STYLE}" == "${BRODEAU_eNATL}" ]; then
        for file in $(ls ${SDIR}/${CONFIG}-${CASE}*-S/*/${CONFIG}-${CASE}*_${FREQ}_*_${TYP}_${YYYY}${MM}??-${YYYY}${MM}??.nc); do
                day=$(basename $file | awk -F_ '{print $6}' | awk -F- '{print $2}' | awk -F. '{print $1}')
                DD=$(echo "${day: -2}")
                fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done
fi

if [ "${STYLE}" == "${JMB}" ]; then
        for file in $(ls ${SDIR}/${CONFIG}${CASE}_y${YYYY}m${MM}d*.${FREQ}_${TYP}.nc); do
		fileo=$(basename $file | sed "s/${TYP}/${VAR}/g")
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done
fi

if [ "${STYLE}" == "${BRODEAU_eNATL_SPINUP}" ]; then
	for file in $(find ${SDIR}/${CONFIG}-${CASE}*-S/* -name ${CONFIG}-${CASE}*_${FREQ}_${YYYY}${MM}??*_${TYP}.nc); do 
                day1=$(basename $file | awk -F_ '{print $3}')
                day2=$(basename $file | awk -F_ '{print $4}')
                fileo=${CONFIG}${SREG}-${CASE}_${day1}-${day2}.${FREQ}_${VAR}.nc
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done
	for file in $(find ${SDIR}/${CONFIG}-${CASE}*-S/* -name ${CONFIG}-${CASE}*_${FREQ}_*_${TYP}_${YYYY}${MM}??-${YYYY}${MM}??.nc); do
                day=$(basename $file | awk -F_ '{print $6}' | awk -F- '{print $2}' | awk -F. '{print $1}')
                DD=$(echo "${day: -2}")
                fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc
                if [ ! -f  $fileo ]; then
                        echo $fileo
                        NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 -v ${VARNAME} $file $fileo
                fi
        done

fi

