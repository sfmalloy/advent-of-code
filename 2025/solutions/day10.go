package solutions

import (
	"container/list"
	"io"
	"os"
	"strconv"
	"strings"
)

type Day10 struct{}

type ButtonData struct {
	buttons     []int
	endState    int
	endCounters []int
}

func (d Day10) Parse(file *os.File, part int) ([]ButtonData, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	datas := []ButtonData{}
	for line := range strings.Lines(string(data)) {
		buttonData := ButtonData{}

		parts := strings.Split(strings.Trim(line, "\n"), " ")

		endState := parts[0]
		buttonData.endState = 0
		for _, char := range endState[1 : len(endState)-1] {
			buttonData.endState <<= 1
			if char == '#' {
				buttonData.endState |= 1
			}
		}

		L := len(endState) - 2
		buttonData.buttons = make([]int, len(parts)-2)
		for b, buttonDef := range parts[1 : len(parts)-1] {
			indices := map[int]bool{}
			for i := range strings.SplitSeq(buttonDef[1:len(buttonDef)-1], ",") {
				index, err := strconv.Atoi(i)
				if err != nil {
					return nil, err
				}
				indices[index] = true
			}
			button := 0
			for i := range L {
				button <<= 1
				if indices[i] {
					button |= 1
				}
			}
			buttonData.buttons[b] = button

			if part == 2 {
				button := 0
				for range L {
					button <<= 1
					button |= buttonData.buttons[b] & 1
					buttonData.buttons[b] >>= 1
				}
				buttonData.buttons[b] = button
			}
		}

		counterDef := parts[len(parts)-1]
		buttonData.endCounters = []int{}
		for i := range strings.SplitSeq(counterDef[1:len(counterDef)-1], ",") {
			count, err := strconv.Atoi(i)
			if err != nil {
				return nil, err
			}
			buttonData.endCounters = append(buttonData.endCounters, count)
		}
		datas = append(datas, buttonData)
	}

	return datas, nil
}

type ButtonNode[T int | []int] struct {
	presses      int
	state        T
	pressedIndex int
}

func (d Day10) Part1(data []ButtonData) int {
	results := make(chan int, len(data))
	for _, machine := range data {
		go lightSearch(machine, results)
	}

	presses := 0
	for range len(data) {
		presses += <-results
	}
	return presses
}

func (d Day10) Part2(data []ButtonData) int {
	return 0
}

func lightSearch(machine ButtonData, res chan int) {
	q := list.New()
	q.PushBack(ButtonNode[int]{presses: 0, state: 0})
	for q.Len() > 0 {
		curr := q.Remove(q.Front()).(ButtonNode[int])
		if curr.state == machine.endState {
			res <- curr.presses
			break
		}
		for _, button := range machine.buttons {
			q.PushBack(ButtonNode[int]{presses: curr.presses + 1, state: curr.state ^ button})
		}
	}
}
