all: 1 2 3

1: Day01.s
	gcc -m64 -g -no-pie $^ -o Day01

2: Day02.hs
	ghc $^

3: Day03.go
	go build $^

clean:
	$(RM) *.o *.hi
	$(RM) Day01 Day02 Day03
