package solutions

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/mat"
)

type Day10 struct{}

type ButtonData struct {
	part1Buttons       []int
	part2Buttons       [][]bool
	endLights          int
	endCounters        []int
	unfinishedCounters [][]bool
	id                 int
}

func (d Day10) Parse(file *os.File, part int) ([]ButtonData, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	for line := range strings.Lines(string(data)) {
		line = strings.Trim(line, "\n")
		parts := strings.Split(line, " ")
		buttons := [][]int{}
		for _, buttonDef := range parts[1 : len(parts)-1] {
			buttonDef = buttonDef[1 : len(buttonDef)-1]
			button, err := numArray(strings.Split(buttonDef, ","))
			if err != nil {
				return nil, err
			}
			buttons = append(buttons, button)
		}

		counterDef := parts[len(parts)-1]
		counters, err := numArray(strings.Split(counterDef[1:len(counterDef)-1], ","))
		if err != nil {
			return nil, err
		}

		mData := make([]float64, len(counters)*(len(buttons)+1))
		m := mat.NewDense(len(counters), len(buttons)+1, mData)
		m.Zero()
		for r, counter := range counters {
			m.Set(r, len(buttons), float64(counter))
		}
		for c, indices := range buttons {
			for _, r := range indices {
				m.Set(r, c, 1.0)
			}
		}

		fmt.Println(mat.Formatted(m))
		var a mat.SymDense
		a.SymOuterK(1, m)

		// i := 0
		// for _, button := range buttons {
		// 	fmt.Println(button)
		// 	for _, idx := range button {
		// 		mData[i+idx] = 1.0
		// 	}
		// 	mData[i+len(counters)] = counters[]
		// 	i += len(counters) + 1
		// }
		fmt.Println()
	}

	return nil, nil
}

func numArray(S []string) ([]int, error) {
	nums := make([]int, len(S))
	for i, s := range S {
		n, err := strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
		nums[i] = n
	}
	return nums, nil
}

type ButtonNode[T int | []int] struct {
	presses      int
	state        T
	pressedIndex int
}

func (d Day10) Part1(data []ButtonData) int {
	return 0
}

func (d Day10) Part2(data []ButtonData) int {
	return 0
}
