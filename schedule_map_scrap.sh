#!/bin/bash

declare -a arr=(
"https://www.google.com/maps/search/Dog+Boarding+OR+Dog+Daycare+OR+Dog+Overnight+OR+Pet+Boarding+OR+Pet+Daycare/@33.3934384,-91.1301712,12z/data=\!3m1\!4b1\!4m8\!2m7\!3m6\!1sDog+Boarding+OR+Dog+Daycare+OR+Dog+Overnight+OR+Pet+Boarding+OR+Pet+Daycare\!2sGreenville,+MS,+USA\!3s0x862befcdb7aec9fb:0x5e8e481acf45111\!4m2\!1d-91.0377029\!2d33.399661"

"https://www.google.com/maps/search/Dog+Boarding/@33.3933991,-91.1301714,12z/data=\!3m1\!4b1\!4m8\!2m7\!3m6\!1sDog+Boarding\!2sGreenville,+MS,+USA\!3s0x862befcdb7aec9fb:0x5e8e481acf45111\!4m2\!1d-91.0377029\!2d33.399661"
)

for i in "${arr[@]}"
do
   echo "$i" | python3 map_latest.py
   sleep 30
done
