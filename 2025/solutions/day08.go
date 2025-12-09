package solutions

import (
	"io"
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

type VecPair Pair[Vec3, Vec3]

type Distance struct {
	dist int
	pair VecPair
}

func Sort(D []Distance) {
	slices.SortFunc(D, func(a, b Distance) int {
		if a.dist < b.dist {
			return -1
		} else if a.dist > b.dist {
			return 1
		}
		return 0
	})
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

func (d Day08) Part1(boxes []Vec3) any {
	D := []Distance{}
	connections := map[Vec3][]Vec3{}
	for i, a := range boxes {
		for _, b := range boxes[i+1:] {
			D = append(D, Distance{pair: VecPair{a, b}, dist: a.Dist(b)})
		}
		connections[a] = []Vec3{}
	}
	Sort(D)
	count := 0
	for _, node := range D {
		connections[node.pair.first] = append(connections[node.pair.first], node.pair.second)
		connections[node.pair.second] = append(connections[node.pair.second], node.pair.first)
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

func (d Day08) Part2(boxes []Vec3) any {
	D := []Distance{}
	connections := map[Vec3][]Vec3{}
	for i, a := range boxes {
		for _, b := range boxes[i+1:] {
			D = append(D, Distance{pair: VecPair{a, b}, dist: a.Dist(b)})
		}
		connections[a] = []Vec3{}
	}
	Sort(D)

	answer := 0
	for _, node := range D {
		connections[node.pair.first] = append(connections[node.pair.first], node.pair.second)
		connections[node.pair.second] = append(connections[node.pair.second], node.pair.first)

		largest := 0
		seen := map[Vec3]bool{}
		for k := range connections {
			t := visit(k, 0, connections, seen)
			if t > 0 {
				largest = max(largest, t)
			}
		}
		if largest == len(boxes) {
			answer = node.pair.first.x * node.pair.second.x
			break
		}
	}
	return answer
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
