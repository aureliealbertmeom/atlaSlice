#!/bin/bash

for box in LS; do
	case $box in
		GS) kk=109;;
		LS) kk=65;;
		MNA) kk=399;;
	esac
	for k in $(seq 0 $kk); do
		cp script_template_extract_anna_profiles.ksh tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNAME/$box/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNUMBER/$k/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		chmod +x tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		echo "$k ./tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh" >> tmp_mpmd_extract_anna_profiles_LS.ksh
	done
done

chmod +x tmp_mpmd_extract_anna_profiles_LS.ksh
