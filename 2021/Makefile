all: 16

1: Day01.s
	@gcc -m64 -g -no-pie $^ -o Day01

2: Day02.hs
	@ghc -v0 $^

3: Day03.go
	@go build $^

4: Day04.java
	@javac $^

6: Day06.c
	@gcc $^ -O2 -o Day06

7: Day07.kt
	@kotlinc $^ -include-runtime -d Day07.jar

10: Day10.swift
	@swiftc $^

13: Day13.rs
	@rustc Day13.rs

15: Day15.cpp
	@g++ -O2 Day15.cpp -o Day15

16: Day16.ml
	@ocamlc -o Day16 Day16.ml

clean:
	$(RM) *.o *.hi *.class a.out *.jar *.cmi *.cmo
	$(RM) Day01 Day02 Day03 Day06 Day10 Day13 Day15 Day16
