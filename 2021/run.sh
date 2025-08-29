#!/usr/bin/bash

if [ "$#" -ne 1 ]
then
    ./Day01
    echo
    ./Day02
    echo
    ./Day03
    echo
    java Day04
    echo
    ruby Day05.rb
    echo
    ./Day06
    echo
    java -jar Day07.jar
    echo
    node Day08.js
    echo
    julia Day09.jl
    echo
    ./Day10
    echo
    perl Day11.pl
    echo
    clisp Day12.lisp
    echo
    ./Day13
    echo
    ts-node Day14.ts
    echo
    ./Day15
    echo
    dotnet-script Day16.csx
    echo
    Rscript Day17.R
    echo
    python Day18.py
elif [ $1 -eq 1 ]
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
elif [ $1 -eq 11 ]
then
    perl Day11.pl
elif [ $1 -eq 12 ]
then
    clisp Day12.lisp
elif [ $1 -eq 13 ]
then
    ./Day13
elif [ $1 -eq 14 ]
then
    npm run build
    npm run day14
elif [ $1 -eq 15 ]
then
    ./Day15
elif [ $1 -eq 16 ]
then
    dotnet-script Day16.csx
elif [ $1 -eq 17 ]
then
    Rscript Day17.R
elif [ $1 -eq 18 ]
then
    python Day18.py
elif [ $1 -eq 19 ]
then
    npm run day19
elif [ $1 -eq 20 ]
then
    php Day20.php
elif [ $1 -eq 21 ]
then
    lua Day21.lua
else
    echo "Day not found"
fi
