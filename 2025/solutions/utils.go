package solutions

import "math"

func magnitude[T int | int64](x T) int {
	return int(math.Floor(math.Log10(float64(x)))) + 1
}

type Pair[A any, B any] struct {
	first  A
	second B
}

type Vec2 struct {
	r int
	c int
}

func (v Vec2) Add(other Vec2) Vec2 {
	return Vec2{v.r + other.r, v.c + other.c}
}

func (v Vec2) Sub(other Vec2) Vec2 {
	return Vec2{v.r - other.r, v.c - other.c}
}

func iAbs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
