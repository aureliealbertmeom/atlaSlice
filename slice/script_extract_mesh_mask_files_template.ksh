#!/bin/bash

CONFIG=CONFIGURATION
REG=REGIONNAME
SREG=REGIONABR
SDIR=SOURCEDIR
MESHH=MESHHFILE
MESHZ=MESHZFILE
MASK=MASKFILE
BATHY=BATHYFILE
X1=XX1
X2=XX2
Y1=YY1
Y2=YY2

TDIR=SCPATH/${CONFIG}/${CONFIG}-I
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

for file in $MESHH $MESHZ $MASK $BATHY; do
	fileo=$(basename $file | sed "s/${CONFIG}/${CONFIG}${SREG}/g")
	if [ ! -f  $fileo ]; then
		echo $fileo
		NCOPATH/ncks -O -F -d x,$X1,$X2 -d y,$Y1,$Y2 $file $fileo
	fi
done


