package solutions

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type Day09 struct{}

func (d Day09) Parse(file *os.File, part int) ([]Vec2, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	tiles := []Vec2{}
	for line := range strings.Lines(string(data)) {
		pair := strings.Split(strings.Trim(line, "\n"), ",")
		tile := Vec2{}
		tile.r, err = strconv.Atoi(pair[0])
		if err != nil {
			return nil, err
		}
		tile.c, err = strconv.Atoi(pair[1])
		if err != nil {
			return nil, err
		}
		tiles = append(tiles, tile)
	}
	return tiles, nil
}

func (d Day09) Part1(tiles []Vec2) int {
	largest := 0
	for i, a := range tiles {
		for _, b := range tiles[i+1:] {
			diff := a.Sub(b)
			diff.r = iAbs(diff.r) + 1
			diff.c = iAbs(diff.c) + 1
			largest = max(largest, diff.r*diff.c)
		}
	}
	return largest
}

type TileRange Pair[int, int]

func (d Day09) Part2(tiles []Vec2) int {
	// validR := map[int][]TileRange{}
	// validC := map[int][]TileRange{}
	// mn := Vec2{1000000000000, 1000000000000}
	// mx := Vec2{0, 0}
	// for _, t := range tiles {
	// 	if t.r < mn.r {
	// 		mn.r = t.r
	// 	}
	// 	if t.r > mx.r {
	// 		mx.r = t.r
	// 	}
	// 	if t.c < mn.c {
	// 		mn.c = t.c
	// 	}
	// 	if t.c > mx.c {
	// 		mx.c = t.c
	// 	}
	// }

	edges := map[Vec2]bool{}
	for i := range tiles {
		a := tiles[i]
		b := tiles[(i+1)%len(tiles)]
		var delta Vec2
		if a.r == b.r {
			delta = Vec2{0, (a.c - b.c) / iAbs(a.c-b.c)}
		} else {
			delta = Vec2{(a.r - b.r) / iAbs(a.r-b.r), 0}
		}
		curr := b
		for curr != a {
			edges[curr] = true
			curr = curr.Add(delta)
		}
		edges[a] = true
	}

	for r := range 13 {
		for c := range 13 {
			found := false
			for _, t := range tiles {
				v := Vec2{r, c}
				if t == v {
					found = true
					break
				}
			}
			if found {
				fmt.Print("#")
			} else if edges[Vec2{r, c}] {
				fmt.Print("X")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}

	largest := 0
	for i, a := range tiles {
		for _, b := range tiles[i+1:] {
			u := Vec2{a.r, b.c}
			v := Vec2{b.r, a.c}
			if !validateEdge(a, u, edges) ||
				!validateEdge(u, b, edges) ||
				!validateEdge(b, v, edges) ||
				!validateEdge(v, a, edges) {
				fmt.Println("invalid ", a, u, b, v)
				continue
			}
			diff := a.Sub(b)
			diff.r = iAbs(diff.r) + 1
			diff.c = iAbs(diff.c) + 1
			largest = max(largest, diff.r*diff.c)
		}
	}

	return largest
}

func validateEdge(a Vec2, b Vec2, edges map[Vec2]bool) bool {
	if a == b {
		return true
	}
	var delta Vec2
	if a.r == b.r {
		delta = Vec2{0, (a.c - b.c) / iAbs(a.c-b.c)}
	} else {
		delta = Vec2{(a.r - b.r) / iAbs(a.r-b.r), 0}
	}
	curr := b
	for curr != a {
		if !edges[curr] {
			fmt.Println(curr)
			return false
		}
		curr = curr.Add(delta)
	}

	return true
}
