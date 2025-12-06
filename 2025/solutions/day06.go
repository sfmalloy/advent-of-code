package solutions

import (
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Day06 struct{}

type Homework struct {
	nums [][]int64
	ops  []byte
}

func (d Day06) Parse(file *os.File, part int) (*Homework, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(data), "\n")
	problems := &Homework{nums: make([][]int64, 0), ops: make([]byte, 0)}
	if part == 1 {
		numTest := regexp.MustCompile(`\d+`)
		for i, line := range lines[:len(lines)-2] {
			row := numTest.FindAll([]byte(line), -1)
			if i == 0 {
				for range len(row) {
					problems.nums = append(problems.nums, make([]int64, 0))
				}
			}
			for i, num := range row {
				if len(strings.Trim(string(num), "\n ")) == 0 {
					continue
				}
				num, err := strconv.ParseInt(string(num), 10, 64)
				if err != nil {
					return nil, err
				}
				problems.nums[i] = append(problems.nums[i], num)
			}
		}
	} else {
		newLines := make([]string, len(lines[0]))
		for _, line := range lines[:len(lines)-2] {
			for i, char := range line {
				newLines[i] += string(char)
			}
		}

		block := 0
		for _, line := range newLines {
			trimmed := strings.Trim(line, "\n ")
			if len(trimmed) == 0 {
				block += 1
			} else {
				num, err := strconv.ParseInt(trimmed, 10, 64)
				if err != nil {
					return nil, err
				}
				if len(problems.nums) == block {
					problems.nums = append(problems.nums, make([]int64, 0))
				}
				problems.nums[block] = append(problems.nums[block], num)
			}
		}
	}

	opTest := regexp.MustCompile(`[*+]`)
	ops := opTest.FindAll([]byte(lines[len(lines)-2]), -1)
	problems.ops = make([]byte, len(ops))
	for i, op := range ops {
		problems.ops[i] = op[0]
	}
	return problems, nil
}

func (d Day06) Part1(problems *Homework) int64 {
	return solve(problems)
}

func (d Day06) Part2(problems *Homework) int64 {
	return solve(problems)
}

func solve(problems *Homework) int64 {
	var total int64 = 0
	for i, prob := range problems.nums {
		if problems.ops[i] == '+' {
			var answer int64 = 0
			for _, num := range prob {
				answer += num
			}
			total += answer
		} else {
			var answer int64 = 1
			for _, num := range prob {
				answer *= num
			}
			total += answer
		}
	}
	return total
}
