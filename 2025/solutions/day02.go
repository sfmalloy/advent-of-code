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
			parts, L := splitNum(num, 2)
			if L == 0 {
				continue
			}
			if parts[0] == parts[1] {
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
			numlen := magnitude(num)
			for numSplits := 2; numSplits <= numlen; numSplits++ {
				parts, L := splitNum(num, numSplits)
				if L == 0 {
					continue
				}
				equal := true
				for i := range L {
					if i == 0 || parts[i] == 0 {
						continue
					}
					equal = equal && parts[i] == parts[i-1]
				}
				if equal {
					total += int64(num)
					break
				}
			}
		}
	}
	return total
}

const LIMIT = 12

func splitNum(x int, numSplits int) ([LIMIT]int, int) {
	parts := [LIMIT]int{}
	if magnitude(x)%numSplits != 0 {
		return parts, 0
	}
	pow := int(math.Pow10(magnitude(x) / numSplits))
	L := 0
	for x > 0 {
		parts[L] = x % pow
		x /= pow
		L += 1
		if pow == 1 {
			break
		}
	}
	return parts, L + 1
}

func magnitude(x int) int {
	return int(math.Floor(math.Log10(float64(x)))) + 1
}
