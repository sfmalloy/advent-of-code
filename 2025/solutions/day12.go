package solutions

import (
	"io"
	"os"
)

type Day12 struct{}

func (d Day12) Parse(file *os.File) (string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (d Day12) Part1(input string) int {
	return 1
}

func (d Day12) Part2(input string) int {
	return 2
}
