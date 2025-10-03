package solutions

import (
	"io"
	"os"
)

type Day23 struct{}

func (d Day23) Parse(file *os.File) (string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (d Day23) Part1(input string) int {
	return 1
}

func (d Day23) Part2(input string) int {
	return 2
}
