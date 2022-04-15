#!/bin/bash
## Categorie,Naam van het fragment?,PID van het fragment?,Datum,Starttijd ,Eindtijd,Duration [s],Link naar archief,Waarom interessant?,Gekozen door?,Opmerkingen,Downloaded,Transcriptie done,Transcriptie gevalideerd

while IFS="," read -r Categorie Naam_van_het_fragment PID Datum Starttijd Eindtijd Duration Link_naar_archief Waarom_interessant Gekozen_door Opmerkingen Downloaded Transcriptie_done Transcriptie_gevalideerd
#while read line
do
   echo "Record is : $PID"
   if [[ ! -z $PID ]] ;then
        START=`timecode_convert -v $Starttijd -s 0 -r 25 2>/dev/null`
        END=`timecode_convert -v $Eindtijd -s 0 -r 25 2> /dev/null`
	mkdir ${Categorie} 2> /dev/null || echo target dir  exists 
	if [[ ! -f ${Categorie}/${Naam_van_het_fragment} ]];then
	    mediahaven_partial -p ${PID}  -s ${START} -e ${END} -f ${Categorie}/${Naam_van_het_fragment}
	else echo file exists
	fi
   else echo could not parse ${PID}
   fi

done < <(tail -n +1 example_csv)
