package solutions

import "math"

func magnitude[T int | int64](x T) int {
	return int(math.Floor(math.Log10(float64(x)))) + 1
}
