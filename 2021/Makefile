all: 1 2 3 4 6 7 10

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

clean:
	$(RM) *.o *.hi *.class a.out *.jar
	$(RM) Day01 Day02 Day03 Day06 Day10
