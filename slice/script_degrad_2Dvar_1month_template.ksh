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
RR=RATIO
PT=VARTYP

SDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}
TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}-degrad${RR}/${FREQ}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

ulimit -s unlimited

if [ ! -f mask.nc ]; then
	cp MASKFILE mask.nc
fi

if [ ! -f mesh_hgr.nc ]; then
	cp MESHHFILE mesh_hgr.nc
fi

if [ ! -f mesh_zgr.nc ]; then
	cp MESHZFILE mesh_zgr.nc
fi

for file in $(ls ${SDIR}/${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d??.${FREQ}_${VAR}.nc); do
	fileo=$(basename $file | sed "s/${VAR}/${VAR}-degrad${RR}/g")
	if [ ! -f  $fileo ]; then
		echo $fileo
		CDFPATH/cdfdegrad -f ${file} -v ${VARNAME} -r $RR $RR -p ${PT} -o ${fileo}
	fi
done

