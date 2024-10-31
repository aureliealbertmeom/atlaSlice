#!/bin/bash

CONFIG=CONFIGURATION
REG=REGIONNAME
SREG=REGIONABR
SDIR=SOURCEDIR
XY="XTRACTINDICES"
MESHH=MESHHFILE
MESHZ=MESHZFILE
MASK=MASKFILE

TDIR=SCPATH/${CONFIG}/${CONFIG}-I/${REG}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

for file in $MESHH $MESHZ $MASK; do
	fileo=$(basename $file | sed "s/${CONFIG}/${CONFIG}${SREG}/g")
	if [ ! -f  $fileo ]; then
		echo $fileo
		NCOPATH/ncks -O -F ${XY} $file $fileo
	fi
done


