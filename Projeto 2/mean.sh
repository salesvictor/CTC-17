#!/bin/sh

for file in $(ls *.csv)
do
  awk -F ',' -v file="$file" '{sum += $2; sumsq += $2*$2 n++} END {print file ":" sum/n ":" sqrt((sumsq-(sum*sum)/n)/n)}' $file
done
