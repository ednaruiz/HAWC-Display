#!/bin/bash
#Bash script for reading HAWC raw data, parsing it to .root and reading it with the executalbe MH.
#Edna Ruiz

eval `$HAWCSOFT/setup.sh`
export CONFIG_HAWC=~/hawc_software/config-hawc

userhome=~

year=
month=

until [ -z "$1" ]; do
    case "$1" in
        -y|--year) shift; year="$1"; shift ;;
        -m|--month) shift; month="$1"; shift ;;
        -h|--help) shift; echo "-y Year[13,14,15..] -m Month[01,...,12]"; shift;;
        -*) shift ;;
        *) break ;;
    esac
done

if [ ! $year ] || [ ! $month ];then
echo ""
echo "year and/or month not specified"
echo "run sh readHAWC.sh -h for help"
echo ""
exit 1
fi


mkdir $userhome/$year$month

echo "Accesing to HAWC data"
RAW_DATA=data/hawc/data

cd $HAWCROOT/$RAW_DATA/$year/$month/


for i in $(ls -d */)
do 
	cd $i
	for f in *.dat
	do
		rawdir=$HAWCROOT/$RAW_DATA/$year/$month
		out=${f%????}.root
		echo "Executing: online-hit-dump -c $CONFIG_HAWC -o $userhome/$year$month/$out --input $rawdir/$i$f"
		online-hit-dump -c $CONFIG_HAWC -o $userhome/$year$month/$out --input $rawdir/$i$f

	done
	cd ..
done
