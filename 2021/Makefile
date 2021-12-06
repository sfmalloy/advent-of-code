all: 6

1: Day01.s
	gcc -m64 -g -no-pie $^ -o Day01

2: Day02.hs
	ghc $^

3: Day03.go
	go build $^

4: Day04.java
	javac $^

6: Day06.c
	gcc -g $^ -o Day06

clean:
	$(RM) *.o *.hi *.class a.out
	$(RM) Day01 Day02 Day03 Day06
