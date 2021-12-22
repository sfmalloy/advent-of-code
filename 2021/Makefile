all: 20

1: Day01.s
	@echo "Compiling Day01.s..."
	@gcc -m64 -g -no-pie $^ -o Day01

2: Day02.hs
	@echo "Compiling Day02.hs..."
	@ghc -v0 $^

3: Day03.go
	@echo "Compiling Day03.go..."
	@go build $^

4: Day04.java
	@echo "Compiling Day04.java..."
	@javac $^

6: Day06.c
	@echo "Compiling Day06.c..."
	@gcc $^ -O2 -o Day06

7: Day07.kt
	@echo "Compiling Day07.kt..."
	@kotlinc $^ -include-runtime -d Day07.jar

10: Day10.swift
	@echo "Compiling Day10.swift..."
	@swiftc $^

13: Day13.rs
	@echo "Compiling Day13.rs..."
	@rustc Day13.rs

15: Day15.cpp
	@echo "Compiling Day15.cpp..."
	@g++ -O2 Day15.cpp -o Day15

20: Day20.d
	@echo "Compiling Day20.d..."
	@dmd $^ -ofDay20

clean:
	$(RM) *.o *.hi *.class a.out *.jar *.cmi *.cmo
	$(RM) Day01 Day02 Day03 Day06 Day10 Day13 Day15 Day16
