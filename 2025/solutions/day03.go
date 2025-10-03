package solutions

import (
	"io"
	"os"
)

type Day03 struct{}

func (d Day03) Parse(file *os.File) (string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (d Day03) Part1(input string) int {
	return 1
}

func (d Day03) Part2(input string) int {
	return 2
}
