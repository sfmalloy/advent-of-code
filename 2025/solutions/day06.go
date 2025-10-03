package solutions

import (
	"io"
	"os"
)

type Day06 struct{}

func (d Day06) Parse(file *os.File) (string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (d Day06) Part1(input string) int {
	return 1
}

func (d Day06) Part2(input string) int {
	return 2
}
