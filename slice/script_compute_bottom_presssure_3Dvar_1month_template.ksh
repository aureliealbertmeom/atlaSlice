#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
FREQ=FREQUENCY
YYYY=YEAR
MM=MONTH

TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}-S/${FREQ}/${REG}
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

SDIR=SOURCEDIR/${FREQ}/${YEAR}

for file in $(ls $SDIR/${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}.${FREQ}_gridT.nc); do
	fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}.${FREQ}_BOTPRES.nc
	if [ ! -f  $fileo ]; then
		echo $fileo
		CDFPATH/cdfbotpressure -t ${file} -teos10 -nc4 -o tmp_${fileo}
		mv tmp_${fileo} ${fileo}
	fi
done

