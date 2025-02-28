#!/bin/bash

for box in MNA; do
	case $box in
		GS) kk=109;;
		LS) kk=65;;
		MNA) kk=399;;
	esac
	for k in $(seq 0 127); do
		cp script_template_extract_anna_profiles.ksh tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNAME/$box/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNUMBER/$k/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		chmod +x tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		echo "$k ./tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh" >> tmp_mpmd1_extract_anna_profiles_MNA.ksh
	done
	for k in $(seq 128 255); do
		cp script_template_extract_anna_profiles.ksh tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNAME/$box/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNUMBER/$k/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		chmod +x tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		kkk=`expr $k - 128`
		echo "$kkk ./tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh" >> tmp_mpmd2_extract_anna_profiles_MNA.ksh
	done
	for k in $(seq 256 383); do
		cp script_template_extract_anna_profiles.ksh tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNAME/$box/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNUMBER/$k/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		chmod +x tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		kkk=`expr $k - 256`
		echo "$kkk ./tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh" >> tmp_mpmd3_extract_anna_profiles_MNA.ksh
	done
	for k in $(seq 384 $kk); do
		cp script_template_extract_anna_profiles.ksh tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNAME/$box/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		sed -i "s/BOXNUMBER/$k/g" tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		chmod +x tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh
		kkk=`expr $k - 384`
		echo "$kkk ./tmp_script_extract_anna_profiles_${box}_${k}_200907.ksh" >> tmp_mpmd4_extract_anna_profiles_MNA.ksh
	done
done

chmod +x tmp_mpmd1_extract_anna_profiles_MNA.ksh
chmod +x tmp_mpmd2_extract_anna_profiles_MNA.ksh
chmod +x tmp_mpmd3_extract_anna_profiles_MNA.ksh
chmod +x tmp_mpmd4_extract_anna_profiles_MNA.ksh
