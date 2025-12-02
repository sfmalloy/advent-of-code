package solutions

import (
	"io"
	"math"
	"os"
	"strconv"
	"strings"
)

type Day02 struct{}

type Range struct {
	start int
	end   int
}

func (d Day02) Parse(file *os.File) ([]Range, error) {
	ranges := make([]Range, 0)
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	for line := range strings.SplitSeq(strings.Trim(string(data), "\n"), ",") {
		if len(line) == 0 {
			continue
		}
		parts := strings.SplitN(line, "-", 2)
		a, err := strconv.Atoi(parts[0])
		if err != nil {
			return nil, err
		}
		b, err := strconv.Atoi(parts[1])
		if err != nil {
			return nil, err
		}
		ranges = append(ranges, Range{start: a, end: b})
	}
	return ranges, nil
}

func (d Day02) Part1(ranges []Range) int64 {
	var total int64 = 0
	for _, rng := range ranges {
		for num := rng.start; num <= rng.end; num++ {
			if equalChunks(num, magnitude(num), 2) {
				total += int64(num)
			}
		}
	}
	return total
}

func (d Day02) Part2(ranges []Range) int64 {
	var total int64 = 0
	for _, rng := range ranges {
		for num := rng.start; num <= rng.end; num++ {
			mag := magnitude(num)
			for numChunks := 2; numChunks <= mag; numChunks++ {
				if equalChunks(num, mag, numChunks) {
					total += int64(num)
					break
				}
			}
		}
	}
	return total
}

func equalChunks(num int, mag int, numChunks int) bool {
	if mag%numChunks != 0 {
		return false
	}

	parts := [12]int{}
	pow := int(math.Pow10(mag / numChunks))
	L := 0
	for num > 0 {
		parts[L] = num % pow
		num /= pow
		L += 1
		if pow == 1 {
			break
		}
	}

	for i := range L {
		if i == 0 || parts[i] == 0 {
			continue
		}
		if parts[i] != parts[i-1] {
			return false
		}
	}
	return true
}

func magnitude(x int) int {
	return int(math.Floor(math.Log10(float64(x)))) + 1
}
