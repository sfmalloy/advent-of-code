package solutions

import (
	"io"
	"os"
)

type Day10 struct{}

func (d Day10) Parse(file *os.File, part int) (string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (d Day10) Part1(input string) int {
	return 1
}

func (d Day10) Part2(input string) int {
	return 2
}
