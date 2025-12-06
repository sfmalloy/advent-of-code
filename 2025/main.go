package main

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/sfmalloy/advent-of-code/2025/lib"
	"github.com/sfmalloy/advent-of-code/2025/solutions"
)

func main() {
	godotenv.Load()
	os.Getenv("AOC_SESSION")
	args := lib.ParseArgs()

	limit := 5

	var err error
	switch args.Day {
	case 0:
		for day := range limit {
			fmt.Printf("Day %d\n", day+1)
			args.Day = day + 1
			err = runSingleDay(args)
			if err != nil {
				fmt.Println(err)
				return
			}
			fmt.Println()
		}
	default:
		err = runSingleDay(args)
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}

func runSingleDay(args lib.RunnerArgs) error {
	var output solutions.SolutionOutput
	var err error

	switch args.Day {
	case 1:
		output, err = solutions.Run(solutions.Day01{}, args)
	case 2:
		output, err = solutions.Run(solutions.Day02{}, args)
	case 3:
		output, err = solutions.Run(solutions.Day03{}, args)
	case 4:
		output, err = solutions.Run(solutions.Day04{}, args)
	case 5:
		output, err = solutions.Run(solutions.Day05{}, args)
	case 6:
		output, err = solutions.Run(solutions.Day06{}, args)
	case 7:
		output, err = solutions.Run(solutions.Day07{}, args)
	case 8:
		output, err = solutions.Run(solutions.Day08{}, args)
	case 9:
		output, err = solutions.Run(solutions.Day09{}, args)
	case 10:
		output, err = solutions.Run(solutions.Day10{}, args)
	case 11:
		output, err = solutions.Run(solutions.Day11{}, args)
	case 12:
		output, err = solutions.Run(solutions.Day12{}, args)
	default:
		fmt.Printf("Invalid day: %d\n", args.Day)
		os.Exit(1)
	}

	if err != nil {
		return err
	}

	if len(output.Part1) > 0 {
		fmt.Printf("Part 1: %s\n", output.Part1)
	}
	if len(output.Part2) > 0 {
		fmt.Printf("Part 2: %s\n", output.Part2)
	}
	fmt.Printf("Time: %.03fms\n", output.Time)

	return nil
}
