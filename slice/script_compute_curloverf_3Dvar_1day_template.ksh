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

if [ ${VARNAME} == vozocrtx ]; then
	VARNAMEV=vomecrty
fi
if [ ${VAR} == U ]; then
	VARV=V
fi


for file in $(ls ${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_${VAR}.nc); do
	files=$(echo $file | sed "s/${VAR}.nc/${VARV}.nc/g")
	fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD}.${FREQ}_curloverf.nc
	if [ ! -f  $fileo ]; then
		echo $fileo
		CDFPATH/cdfcurl -u ${file} ${VARNAME} -v ${files} ${VARNAMEV} -l "1-" -overf -nc4 -o tmp_${fileo}
		mv tmp_${fileo} ${fileo}
	fi
done

