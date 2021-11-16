#!/bin/bash

for i in {1..17}
do
  printf "Day$i\n"
  if [ $i -lt 10 ]
  then
    cd Day0$i/
  else
    cd Day$i/
  fi
  python3 $i.py
  cd ..
  printf "\n"
done