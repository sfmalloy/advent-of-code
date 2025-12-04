package solutions

import (
	"io"
	"os"
)

type Day04 struct{}

func (d Day04) Parse(file *os.File) (map[complex128]byte, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	R := 0
	for col, char := range data {
		if char == '\n' {
			R = col
			break
		}
	}
	floor := make(map[complex128]byte)
	row := 0
	col := 0
	for _, char := range data {
		if char == '\n' {
			continue
		}
		floor[complex(float64(row), float64(col%R))] = char
		col += 1
		if col > 0 && col%R == 0 {
			row += 1
		}
	}
	return floor, nil
}

func (d Day04) Part1(lines map[complex128]byte) int {
	adjacent := [8]complex128{-1 - 1i, 0 - 1i, 1 - 1i, -1, 1, -1 + 1i, 0 + 1i, 1 + 1i}

	count := 0
	for pos, col := range lines {
		if col != '@' {
			continue
		}
		found := 0
		for _, delta := range adjacent {
			neighbor := pos + delta
			if lines[neighbor] == '@' {
				found += 1
			}
		}
		if found < 4 {
			count += 1
		}
	}
	return count
}

func (d Day04) Part2(lines map[complex128]byte) int {
	adjacent := [8]complex128{-1 - 1i, 0 - 1i, 1 - 1i, -1, 1, -1 + 1i, 0 + 1i, 1 + 1i}

	count := 0
	for {
		removable := make([]complex128, 0)

		for pos, col := range lines {
			if col != '@' {
				continue
			}
			found := 0
			for _, delta := range adjacent {
				neighbor := pos + delta
				if lines[neighbor] == '@' {
					found += 1
				}
			}
			if found < 4 {
				removable = append(removable, pos)
				count += 1
			}
		}
		if len(removable) == 0 {
			return count
		}
		for _, pos := range removable {
			lines[pos] = '.'
		}
	}
}
