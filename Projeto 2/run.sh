#!/bin/sh

for i in `seq 1 10`;
do
  echo iteration $i:

  echo Running until_solution
  python3 Problema1.py 4 0 | awk -F ';' '{print $2 "," $3}' | tee -a 4_0.csv
  python3 Problema1.py 5 0 | awk -F ';' '{print $2 "," $3}' | tee -a 5_0.csv
  python3 Problema1.py 6 0 | awk -F ';' '{print $2 "," $3}' | tee -a 6_0.csv
  python3 Problema1.py 7 0 | awk -F ';' '{print $2 "," $3}' | tee -a 7_0.csv
  python3 Problema1.py 8 0 | awk -F ';' '{print $2 "," $3}' | tee -a 8_0.csv

  echo Running max_tries
  python3 Problema1.py 10 1 | awk -F ';' '{print $2 "," $3}' | tee -a 10_1.csv
  python3 Problema1.py 15 1 | awk -F ';' '{print $2 "," $3}' | tee -a 15_1.csv
  python3 Problema1.py 20 1 | awk -F ';' '{print $2 "," $3}' | tee -a 20_1.csv
  python3 Problema1.py 25 1 | awk -F ';' '{print $2 "," $3}' | tee -a 25_1.csv
done
