package solutions

import "math"

func magnitude[T int | int64](x T) int {
	return int(math.Floor(math.Log10(float64(x)))) + 1
}

type Pair[A any, B any] struct {
	first  A
	second B
}
