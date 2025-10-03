package solutions

import "os"

type Day[I any, O any] interface {
	Parse(file *os.File) (I, error)
	Part1(input I) O
	Part2(input I) O
}
