package solutions

import (
	"io"
	"maps"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Day08 struct{}

type Vec3 struct {
	x int
	y int
	z int
}

func (v Vec3) Dist(other Vec3) int {
	dx := v.x - other.x
	dy := v.y - other.y
	dz := v.z - other.z
	return dx*dx + dy*dy + dz*dz
}

func (d Day08) Parse(file *os.File, part int) ([]Vec3, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	boxes := make([]Vec3, 0, 1000)
	for line := range strings.Lines(string(data)) {
		coords := strings.Split(strings.TrimRight(line, "\n"), ",")
		box := Vec3{}
		box.x, err = strconv.Atoi(coords[0])
		if err != nil {
			return nil, err
		}
		box.y, err = strconv.Atoi(coords[1])
		if err != nil {
			return nil, err
		}
		box.z, err = strconv.Atoi(coords[2])
		if err != nil {
			return nil, err
		}
		boxes = append(boxes, box)
	}
	return boxes, nil
}

type VecPair Pair[Vec3, Vec3]

func (d Day08) Part1(boxes []Vec3) any {
	D := map[int]VecPair{}
	connections := map[Vec3][]Vec3{}
	for i, a := range boxes {
		for _, b := range boxes[i+1:] {
			D[a.Dist(b)] = VecPair{a, b}
		}
		connections[a] = []Vec3{}
	}

	count := 0
	for _, a := range slices.Sorted(maps.Keys(D)) {
		best := D[a]
		connections[best.first] = append(connections[best.first], best.second)
		connections[best.second] = append(connections[best.second], best.first)
		count += 1
		if count == 1000 {
			break
		}
	}

	seen := map[Vec3]bool{}
	largest := []int{}
	for k := range connections {
		t := visit(k, 0, connections, seen)
		if t > 0 {
			largest = append(largest, t)
		}
	}
	slices.SortFunc(largest, func(a, b int) int {
		if a < b {
			return 1
		} else if a > b {
			return -1
		}
		return 0
	})

	return largest[0] * largest[1] * largest[2]
}

func visit(curr Vec3, total int, connections map[Vec3][]Vec3, seen map[Vec3]bool) int {
	if seen[curr] {
		return total
	}
	seen[curr] = true
	for _, neighbor := range connections[curr] {
		total = visit(neighbor, total, connections, seen)
	}
	return total + 1
}

func (d Day08) Part2(boxes []Vec3) any {
	D := map[int]VecPair{}
	connections := map[Vec3][]Vec3{}
	for i, a := range boxes {
		for _, b := range boxes[i+1:] {
			D[a.Dist(b)] = VecPair{a, b}
		}
		connections[a] = []Vec3{}
	}

	answer := 0
	for _, a := range slices.Sorted(maps.Keys(D)) {
		best := D[a]
		connections[best.first] = append(connections[best.first], best.second)
		connections[best.second] = append(connections[best.second], best.first)

		largest := 0
		seen := map[Vec3]bool{}
		for k := range connections {
			t := visit(k, 0, connections, seen)
			if t > 0 {
				largest = max(largest, t)
			}
		}
		if largest == len(boxes) {
			answer = best.first.x * best.second.x
			break
		}
	}
	return answer
}
