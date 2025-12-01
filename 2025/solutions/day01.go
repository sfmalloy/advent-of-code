package solutions

import (
	"io"
	"os"
	"strconv"
	"strings"
)

type Day01 struct{}

func (d Day01) Parse(file *os.File) ([]int, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(data), "\n")
	dirs := make([]int, len(lines)-1)
	for i, line := range lines[:len(lines)-1] {
		if len(line) == 0 {
			continue
		}
		dirs[i], err = strconv.Atoi(line[1:])
		if line[0] == 'L' {
			dirs[i] *= -1
		}
	}
	return dirs, nil
}

func (d Day01) Part1(dirs []int) int {
	dial := 50
	password := 0
	for _, dir := range dirs {
		dial = realMod(dir + dial)
		if dial == 0 {
			password += 1
		}
	}
	return password
}

func (d Day01) Part2(dirs []int) int {
	dial := 50
	password := 0
	for _, dir := range dirs {
		for d := 0; d < iAbs(dir); d++ {
			if dir < 0 {
				dial -= 1
			} else {
				dial += 1
			}
			switch dial {
			case 100:
				dial = 0
			case -1:
				dial = 99
			}
			if dial == 0 {
				password += 1
			}
		}
	}
	return password
}

func realMod(dial int) int {
	for dial < 0 {
		dial += 100
	}
	for dial >= 100 {
		dial -= 100
	}
	return dial
}

func iAbs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
