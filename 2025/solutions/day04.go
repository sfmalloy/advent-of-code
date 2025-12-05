package solutions

import (
	"io"
	"os"
)

type Day04 struct{}

func (d Day04) Parse(file *os.File) ([][]byte, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	lines := make([][]byte, 0)
	for i, char := range data {
		if char == '\n' {
			lines = append(lines, make([]byte, i+2))
			break
		}
	}
	row := make([]byte, 1)
	for _, char := range data {
		if char == '\n' {
			row = append(row, 0)
			lines = append(lines, row)
			row = make([]byte, 1)
		} else {
			row = append(row, char)
		}
	}
	lines = append(lines, make([]byte, len(lines[0])))
	return lines, nil
}

func (d Day04) Part1(lines [][]byte) int {
	adjacent := [8]complex128{-1 - 1i, 0 - 1i, 1 - 1i, -1, 1, -1 + 1i, 0 + 1i, 1 + 1i}

	count := 0
	for r, row := range lines {
		for c, col := range row {
			if col != '@' {
				continue
			}
			pos := complex(float64(r), float64(c))
			found := 0
			for _, delta := range adjacent {
				neighbor := pos + delta
				R := int(real(neighbor))
				C := int(imag(neighbor))
				if lines[R][C] == '@' {
					found += 1
				}
			}
			if found < 4 {
				count += 1
			}
		}
	}
	return count
}

func (d Day04) Part2(lines [][]byte) int {
	adjacent := [8]complex128{-1 - 1i, 0 - 1i, 1 - 1i, -1, 1, -1 + 1i, 0 + 1i, 1 + 1i}

	count := 0
	for {
		removable := make([]complex128, 0)
		for r, row := range lines {
			for c, col := range row {
				if col != '@' {
					continue
				}
				pos := complex(float64(r), float64(c))
				found := 0
				for _, delta := range adjacent {
					neighbor := pos + delta
					if lines[int(real(neighbor))][int(imag(neighbor))] == '@' {
						found += 1
					}
				}
				if found < 4 {
					removable = append(removable, pos)
					count += 1
				}
			}
		}
		if len(removable) == 0 {
			return count
		}
		for _, pos := range removable {
			lines[int(real(pos))][int(imag(pos))] = '.'
		}
	}
}
