#!/bin/bash

CONFIG=ORCA025.L75
CASE=OCCITENS.003
REG=global
SREG=
FREQ=1m
YYYY=1996
MM=05

TDIR=/ccc/scratch/cont003/gen12020/alberaur/${CONFIG}/${CONFIG}-${CASE}-S/${FREQ}/${REG}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

SDIR=/ccc/work/cont003/gen12020/alberaur/ORCA025.L75/ORCA025.L75-OCCITENS.003-S/${FREQ}/1996

ulimit -s unlimited

if [ ! -f mask.nc ]; then
	cp /ccc/work/cont003/gen12020/alberaur/ORCA025.L75/ORCA025.L75-I/ORCA025.L75-MJM91_byte_mask.nc mask.nc
fi

if [ ! -f mesh_hgr.nc ]; then
	cp /ccc/work/cont003/gen12020/alberaur/ORCA025.L75/ORCA025.L75-I/ORCA025.L75-MJM91_mesh_hgr.nc mesh_hgr.nc
fi

if [ ! -f mesh_zgr.nc ]; then
	cp /ccc/work/cont003/gen12020/alberaur/ORCA025.L75/ORCA025.L75-I/ORCA025.L75-MJM91_mesh_zgr.nc mesh_zgr.nc
fi



for file in $(ls $SDIR/${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}.${FREQ}_gridT.nc); do
	fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}.${FREQ}_bottom_pressure.nc
	if [ ! -f  $fileo ]; then
		echo $fileo
		/ccc/work/cont003/gen12020/alberaur/DEV/CDFTOOLS/bin/cdfbotpressure -t ${file} -teos10 -nc4 -o tmp_${fileo}
		mv tmp_${fileo} ${fileo}
	fi
done

