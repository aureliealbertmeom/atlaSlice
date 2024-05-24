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
SDIR=SOURCEDIR
STYLE=STYLENOM
TI=INDTI
TF=INDTF
TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

BRODEAU_NST=brodeau_nst
BRODEAU_eNATL=brodeau_enatl
MOLINES=molines
DFS=dfs
ulimit -s unlimited

if [ "${STYLE}" == "${DFS}" ]; then
	for file in $(ls ${SDIR}/drowned_${VARNAME}_${CONFIG}_y${YYYY}.nc); do

		fileo=${CONFIG}${SREG}_y${YYYY}m${MM}.${FREQ}_${VAR}.nc

		if [ ! -f  $fileo ]; then

                        echo $fileo

			if [ ! -f drowned_${VARNAME}_${CONFIG}_y${YYYY}m${MM}.nc ]; then
				ncks -F -d time,$TI,$TF $file drowned_${VARNAME}_${CONFIG}_y${YYYY}m${MM}.nc
			fi

			cp SOSIEPATH/examples/${CONFIG}_to_${SREG}/namelist_sosie_${CONFIG}-${SREG} tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
                	sed -i "s/FILEIN/drowned_${VARNAME}_${CONFIG}_y${YYYY}m${MM}.nc/g" tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
	                sed -i "s/VARIN/${VARNAME}/g" tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
	                sed -i "s/VAROUT/${VARNAME}/g" tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
	                sed -i "s/MASK/MASKNAME/g" tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
	                sed -i "s/DATE/y${YYYY}m${MM}/g" tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
			
			SOSIEPATH/bin/sosie3.x -f tmp_namelist_sosie_${CONFIG}-${SREG}_${VAR}_y${YYYY}m${MM}
	                mv ${VAR}_${CONFIG}-${SREG}_y${YYYY}m${MM}.nc $fileo

		fi
	done
fi


