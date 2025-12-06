package solutions

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/sfmalloy/advent-of-code/2025/lib"
)

type Day[I any, O any] interface {
	Parse(file *os.File, part int) (I, error)
	Part1(input I) O
	Part2(input I) O
}

type SolutionOutput struct {
	Part1 string
	Part2 string
	Time  float64
}

func Run[I any, O any](day Day[I, O], args lib.RunnerArgs) (SolutionOutput, error) {
	output := SolutionOutput{}
	if args.Part == 1 || args.Part == 0 {
		part1, solveTime, err := runPart(day, args.Day, 1, args.InputFile)
		if err != nil {
			return output, err
		}
		output.Part1 = part1
		output.Time += solveTime
	}
	if args.Part == 2 || args.Part == 0 {
		part2, solveTime, err := runPart(day, args.Day, 2, args.InputFile)
		if err != nil {
			return output, err
		}
		output.Part2 = part2
		output.Time += solveTime
	}

	return output, nil
}

func runPart[I any, O any](day Day[I, O], dayNumber int, part int, filename string) (string, float64, error) {
	year, err := strconv.Atoi(os.Getenv("AOC_YEAR"))
	if err != nil {
		return "", 0, err
	}

	input, err := getInputFile(year, dayNumber, filename)
	if err != nil {
		return "", 0, err
	}

	startTime := time.Now()
	parsed, err := day.Parse(input, part)
	if err != nil {
		return "", 0, err
	}
	var output O
	if part == 1 {
		output = day.Part1(parsed)
	} else {
		output = day.Part2(parsed)
	}
	endTime := float64(time.Since(startTime).Microseconds()) / 1000

	return fmt.Sprintf("%v", output), endTime, nil
}

func getInputFile(year int, day int, filename string) (*os.File, error) {
	if len(filename) == 0 {
		return getDefaultInputFile(year, day)
	}
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	return file, nil
}

func getDefaultInputFile(year int, day int) (*os.File, error) {
	filepath := fmt.Sprintf("inputs/day%02d.txt", day)
	file, err := os.Open(filepath)
	if errors.Is(err, os.ErrNotExist) {
		fmt.Println("Downloading input...")
		err = lib.DownloadInput(year, day)
		if err != nil {
			return nil, err
		}

		file, err = os.Open(filepath)
		if err != nil {
			return nil, err
		}
		fmt.Println("Successfully downloaded input")
	} else if err != nil {
		return nil, err
	}
	return file, nil
}
