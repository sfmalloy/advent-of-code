package solutions

import (
	"io"
	"os"
	"strings"
)

type Day03 struct{}

func (d Day03) Parse(file *os.File) ([][]int64, error) {
	data, err := io.ReadAll(file)
	batteries := make([][]int64, 0)
	for line := range strings.Lines(string(data)) {
		battery := make([]int64, len(line)-1)
		for i, char := range strings.Trim(line, "\n") {
			battery[i] = int64(char - '0')
		}
		batteries = append(batteries, battery)
	}
	if err != nil {
		return nil, err
	}
	return batteries, nil
}

func (d Day03) Part1(batteries [][]int64) int64 {
	return totalJoltage(batteries, 2)
}

func (d Day03) Part2(batteries [][]int64) int64 {
	return totalJoltage(batteries, 12)
}

func totalJoltage(batteries [][]int64, size int) int64 {
	var total int64 = 0
	for _, battery := range batteries {
		total += largestJoltage(battery, size)
	}
	return total
}

func largestJoltage(battery []int64, maxSize int) int64 {
	return findJoltage(battery, maxSize, len(battery), 0, 0, 0)
}

func findJoltage(battery []int64, maxSize int, L int, size int, index int, joltage int64) int64 {
	if size == maxSize || index >= L {
		return joltage
	}
	var nextDigit int64 = 0
	for i := index; i < L-(maxSize-size)+1; i++ {
		nextDigit = max(nextDigit, battery[i])
	}
	var best int64 = 0
	for i := index; i < L-(maxSize-size)+1; i++ {
		if battery[i] == nextDigit {
			best = max(best, findJoltage(battery, maxSize, L, size+1, i+1, 10*joltage+nextDigit))
		}
	}
	return best
}
