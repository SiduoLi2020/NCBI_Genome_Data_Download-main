#!/bin/bash
case "$1" in
    -h|--help|?)
    echo "Usage:"
    echo "1st arg: IDtable file from NCBI Assembly"
    echo "2st arg: output file folder name" 
    echo "3st arg: Database(GenBank--GB, Refseq--Ref)"
    echo "Example: bash download.sh IDtable_Mycobacteroides_abscessus.txt Mycobacteroides_abscessus Ref"
    exit 0 
;;
esac

if [ ! -n "$1" ]; then
    echo "pls input 1st arg"
    exit
fi


if [ ! -n "$2" ]; then
    echo "pls input 2st arg"
    exit
fi

if [ ! -n "$3" ]; then
    echo "pls input 3st arg"
    exit
fi


if [[ -f "$2_$3_Context.txt" ]]; then
    echo $2_$3_Context.txt exists!
    echo 
    sleep 1s
else
    python3 makecontext.py -i $1 -n $2 -t $3
    
    sleep 1s

fi

echo +++++++++++++++++++++DOWNLAOD PROCESS++++++++++++++++++++++++++++++++
echo $2_$3_Context.txt is ready! download data from NCBI
sleep 1s

start_time=$(date +%s)

if [[ ! -d $2_$3 ]];then
    mkdir $2_$3/
fi

totalfile=$(wc -l $2_$3_Context.txt | awk '{print $1}')

while read line; do {
    rsync --copy-links --recursive --times --verbose $line $2_$3/ > /dev/null
    
    count=$(ls $2_$3/ | wc -l)
    echo "Downloading + Finished / Toal: $count/$totalfile"
}&  done < $2_$3_Context.txt 

wait

end_time=$(date +%s)
cost_time=$[ $end_time-$start_time ]
echo cost $(($cost_time/60))min $(($cost_time%60))s