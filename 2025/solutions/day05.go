package solutions

import (
	"io"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Day05 struct{}

type FreshRange struct {
	start int64
	end   int64
}

type IngredientData struct {
	freshRanges []FreshRange
	ingredients []int64
}

func (d Day05) Parse(file *os.File) (*IngredientData, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	fresh := make([]FreshRange, 0)
	blocks := strings.Split(string(data), "\n\n")
	for line := range strings.Lines(blocks[0]) {
		mid := strings.Index(line, "-")
		start, err := strconv.ParseInt(line[0:mid], 10, 64)
		if err != nil {
			return nil, err
		}
		end, err := strconv.ParseInt(strings.TrimRight(line[mid+1:], "\n"), 10, 64)
		if err != nil {
			return nil, err
		}
		fresh = append(fresh, FreshRange{start: start, end: end})
	}

	ingredients := make([]int64, 0)
	for line := range strings.Lines(blocks[1]) {
		ingredient, err := strconv.ParseInt(strings.TrimRight(line, "\n"), 10, 64)
		if err != nil {
			return nil, err
		}
		ingredients = append(ingredients, ingredient)
	}

	return &IngredientData{freshRanges: fresh, ingredients: ingredients}, nil
}

func (d Day05) Part1(data *IngredientData) int64 {
	freshCount := 0
	for _, ingredient := range data.ingredients {
		for _, rng := range data.freshRanges {
			if inRange(rng, ingredient) {
				freshCount += 1
				break
			}
		}
	}
	return int64(freshCount)
}

func (d Day05) Part2(data *IngredientData) int64 {
	slices.SortFunc(data.freshRanges, func(a FreshRange, b FreshRange) int {
		if a.start < b.start {
			return -1
		} else if a.start > b.start {
			return 1
		} else if a.end < b.end {
			return -1
		} else if a.end > b.end {
			return 1
		}
		return 0
	})

	var overlap int64 = 0
	for i, a := range data.freshRanges {
		for _, b := range data.freshRanges[i+1:] {
			if inRange(a, b.start) || inRange(a, b.end) {
				start := max(a.start, b.start)
				end := min(a.end, b.end)
				overlap += end - start + 1
				break
			}
		}
	}

	var fresh int64 = 0
	for _, r := range data.freshRanges {
		fresh += r.end - r.start + 1
	}

	return fresh - overlap
}

func inRange(rng FreshRange, test int64) bool {
	return test >= rng.start && test <= rng.end
}
