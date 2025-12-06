package solutions

import (
	"io"
	"os"
)

type Day11 struct{}

func (d Day11) Parse(file *os.File, part int) (string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (d Day11) Part1(input string) int {
	return 1
}

func (d Day11) Part2(input string) int {
	return 2
}
