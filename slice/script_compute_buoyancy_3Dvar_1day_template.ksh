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

SDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}-S/${FREQ}/${REG}
cd $SDIR

echo "We are in " $SDIR

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

if [ ${VARNAME} == votemper ]; then
	VARSAL=vosaline
fi
if [ ${VAR} == T ]; then
	VARS=S
fi


for file in $(ls ${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc); do
	files=$(echo $file | sed "s/${VAR}.nc/${VARS}.nc/g")
	fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_buoyancy.nc
	if [ ! -f  $fileo ]; then
		echo $fileo
		CDFPATH/cdfsig0 -t ${file} -s ${files} -tem ${VARNAME} -sal ${VARSAL} -teos10 -nc4 -o ${fileo}
	fi
done

