#!/usr/bin/bash

if [ $1 -eq 1 ]
then
    ./Day01
elif [ $1 -eq 2 ]
then
    ./Day02
elif [ $1 -eq 3 ]
then
    ./Day03
elif [ $1 -eq 4 ]
then
    java Day04
elif [ $1 -eq 5 ]
then
    ruby Day05.rb
elif [ $1 -eq 6 ]
then
    ./Day06
elif [ $1 -eq 7 ]
then
    java -jar Day07.jar
elif [ $1 -eq 8 ]
then
    node Day08.js
elif [ $1 -eq 9 ]
then
    julia Day09.jl
elif [ $1 -eq 10 ]
then
    ./Day10
else
    echo "Day not found"
fi