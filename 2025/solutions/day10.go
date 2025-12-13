package solutions

import (
	"container/list"
	"fmt"
	"io"
	"os"
	"slices"
	"strconv"
	"strings"
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

	datas := []ButtonData{}
	lineNum := 0
	for line := range strings.Lines(string(data)) {
		buttonData := ButtonData{}
		parts := strings.Split(strings.Trim(line, "\n"), " ")

		if part == 1 {
			end := parts[0]
			buttonData.endLights = 0
			for _, char := range end[1 : len(end)-1] {
				buttonData.endLights <<= 1
				if char == '#' {
					buttonData.endLights |= 1
				}
			}

			L := len(end) - 2
			buttonData.part1Buttons = make([]int, len(parts)-2)
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
				buttonData.part1Buttons[b] = button
			}
		} else {
			L := len(parts[0]) - 2
			buttonData.part2Buttons = make([][]bool, len(parts)-2)
			for b, buttonDef := range parts[1 : len(parts)-1] {
				indices := make([]bool, L)
				for i := range strings.SplitSeq(buttonDef[1:len(buttonDef)-1], ",") {
					index, err := strconv.Atoi(i)
					if err != nil {
						return nil, err
					}
					indices[index] = true
				}
				buttonData.part2Buttons[b] = indices
			}

			buttonData.endCounters = []int{}
			for i := range strings.SplitSeq(parts[len(parts)-1][1:len(parts[len(parts)-1])-1], ",") {
				count, err := strconv.Atoi(i)
				if err != nil {
					return nil, err
				}
				buttonData.endCounters = append(buttonData.endCounters, count)
			}
		}
		buttonData.id = lineNum
		datas = append(datas, buttonData)
		lineNum += 1
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
	t := 0
	for _, d := range data {
		r := counterSearch(d)
		t += r.result
		fmt.Println(r.id, r.result)
	}

	return t
}

type Answer struct {
	result int
	id     int
}

func counterSearch(d ButtonData) Answer {
	slices.SortFunc(d.part2Buttons, func(a, b []bool) int {
		if countTrue(a) < countTrue(b) {
			return 1
		} else if countTrue(a) > countTrue(b) {
			return -1
		} else if countCounters(a, d.endCounters) < countCounters(b, d.endCounters) {
			return -1
		} else if countCounters(a, d.endCounters) > countCounters(b, d.endCounters) {
			return 1
		}
		return 0
	})
	d.unfinishedCounters = make([][]bool, len(d.part2Buttons))
	for i := range d.part2Buttons {
		d.unfinishedCounters[i] = make([]bool, len(d.endCounters))
		for _, button := range d.part2Buttons[i:] {
			for j, b := range button {
				if b {
					d.unfinishedCounters[i][j] = true
				}
			}
		}
	}
	return Answer{result: fill(0, d, make([]int, len(d.endCounters)), 0, INF), id: d.id}
}

func lightSearch(machine ButtonData, res chan int) {
	q := list.New()
	q.PushBack(ButtonNode[int]{presses: 0, state: 0})
	for q.Len() > 0 {
		curr := q.Remove(q.Front()).(ButtonNode[int])
		if curr.state == machine.endLights {
			res <- curr.presses
			break
		}
		for _, button := range machine.part1Buttons {
			q.PushBack(ButtonNode[int]{presses: curr.presses + 1, state: curr.state ^ button})
		}
	}
}

const INF = 100000000000

func fill(buttonIndex int, data ButtonData, state []int, presses int, maxPresses int) int {
	fmt.Println(maxPresses, state)
	if presses >= maxPresses {
		return maxPresses
	}
	if buttonIndex == len(data.part2Buttons) {
		if arrayEqual(data.endCounters, state) {
			fmt.Println(data.id, presses)
			return presses
		}
		return INF
	}
	newCount := state
	for presses < maxPresses {
		if f := fill(buttonIndex+1, data, newCount, presses, maxPresses); f != INF {
			maxPresses = min(f, maxPresses)
		}
		newCount = pressCounterButton(data.part2Buttons[buttonIndex], newCount)
		if !isValidCounts(newCount, data.endCounters) {
			return maxPresses
		}
		for i, c := range data.unfinishedCounters[buttonIndex] {
			if !c && data.endCounters[i] != state[i] {
				return INF
			}
		}
		presses += 1
	}
	return maxPresses
}

func findPossibleCandidates(data ButtonData) int {
	length := 1
	for i, button := range data.part2Buttons {
		t := 0
		counts := make([]int, len(data.endCounters))
		for {
			counts = pressCounterButton(button, counts)
			valid := true
			for j, c := range counts {
				if c > data.endCounters[j] {
					valid = false
					break
				}
			}
			if !valid {
				break
			}
			t += 1
		}
		fmt.Printf("button %d can be pressed up to %d times\n", i, t)
		length *= t
	}
	return length
}

func pressCounterButton(button []bool, counts []int) []int {
	newCounts := make([]int, len(counts))
	for i, b := range button {
		if b {
			newCounts[i] = counts[i] + 1
		} else {
			newCounts[i] = counts[i]
		}
	}
	return newCounts
}

func arrayEqual(a, b []int) bool {
	for i := range len(a) {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func isValidCounts(test, key []int) bool {
	for i := range test {
		if test[i] > key[i] {
			return false
		}
	}
	return true
}

func countTrue(b []bool) int {
	count := 0
	for _, x := range b {
		if x {
			count += 1
		}
	}
	return count
}

func countCounters(b []bool, c []int) int {
	t := 0
	for i, x := range b {
		if x {
			t += c[i]
		}
	}
	return t
}

func printButton(b []bool) {
	for i, x := range b {
		if x {
			fmt.Print(i, ",")
		}
	}
}
