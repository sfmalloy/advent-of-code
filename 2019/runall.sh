#!/bin/bash

for i in {1..15}
do
  printf "Day$i\n"
  if [ $i -lt 10 ]
  then
    cd Day0$i/
  else
    cd Day$i/
  fi
  python $i.py
  cd ..
  printf "\n"
done