package solutions

import (
	"io"
	"math"
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

func (v Vec3) Dist(other Vec3) float64 {
	return math.Sqrt(math.Pow(float64(v.x-other.x), 2) + math.Pow(float64(v.y-other.y), 2) + math.Pow(float64(v.z-other.z), 2))
}

func (v Vec3) Midpoint(other Vec3) Vec3 {
	return Vec3{(v.x + other.x) / 2, (v.y + other.y) / 2, (v.z + other.z) / 2}
}

func (d Day08) Parse(file *os.File, part int) ([]Vec3, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	boxes := make([]Vec3, 0, 1000)
	// boxes := list.New()
	// boxes := map[Vec3]bool{}
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
		// boxes.PushBack(box)
		// boxes[box] = true
	}
	return boxes, nil
}

type VecPair Pair[Vec3, Vec3]

func (d Day08) Part1(boxes []Vec3) any {
	dists := map[Vec3]map[Vec3]float64{}
	connections := map[Vec3][]Vec3{}
	for _, a := range boxes {
		dists[a] = map[Vec3]float64{}
		for _, b := range boxes {
			if a != b {
				dists[a][b] = a.Dist(b)
			}
		}
		connections[a] = []Vec3{}
	}

	for range 1000 {
		shortest := math.Inf(1)
		best := VecPair{}
		for _, a := range boxes {
			for b, dist := range dists[a] {
				if dist < shortest {
					shortest = dist
					best = VecPair{a, b}
				}
			}
		}
		delete(dists[best.first], best.second)
		delete(dists[best.second], best.first)
		connections[best.first] = append(connections[best.first], best.second)
		connections[best.second] = append(connections[best.second], best.first)
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
	dists := map[Vec3]map[Vec3]float64{}
	connections := map[Vec3][]Vec3{}
	for _, a := range boxes {
		dists[a] = map[Vec3]float64{}
		for _, b := range boxes {
			if a != b {
				dists[a][b] = a.Dist(b)
			}
		}
		connections[a] = []Vec3{}
	}

	for {
		shortest := math.Inf(1)
		best := VecPair{}
		for _, a := range boxes {
			for b, dist := range dists[a] {
				if dist < shortest {
					shortest = dist
					best = VecPair{a, b}
				}
			}
		}

		delete(dists[best.first], best.second)
		delete(dists[best.second], best.first)
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
			return best.first.x * best.second.x
		}
	}
}
