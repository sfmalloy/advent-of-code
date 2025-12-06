package main

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
	"github.com/olekukonko/tablewriter"
	"github.com/sfmalloy/advent-of-code/2025/lib"
	"github.com/sfmalloy/advent-of-code/2025/solutions"
)

func main() {
	godotenv.Load()
	os.Getenv("AOC_SESSION")
	args := lib.ParseArgs()

	limit := 12

	outputs := make([]solutions.SolutionOutput, 0)
	switch args.Day {
	case 0:
		for day := range limit {
			args.Day = day + 1
			out, err := runSingleDay(args)
			if err != nil {
				continue
			}
			outputs = append(outputs, out)
		}
	default:
		out, err := runSingleDay(args)
		if err != nil {
			fmt.Println(err)
			return
		}
		outputs = append(outputs, out)
	}

	headers := make([]string, 1)
	headers[0] = "Day"
	rows := make([][]string, 0)
	for _, output := range outputs {
		row := make([]string, 1)
		row[0] = fmt.Sprintf("%d", output.Day)

		if len(output.Part1) > 0 {
			if len(headers) == 1 {
				headers = append(headers, "Part 1")
			}
			row = append(row, output.Part1)
		}
		if len(output.Part2) > 0 {
			if len(headers) <= 2 {
				headers = append(headers, "Part 2")
			}
			row = append(row, output.Part2)
		}
		if len(headers) <= 3 {
			headers = append(headers, "Time(ms)")
		}
		row = append(row, fmt.Sprintf("%.03f", output.Time))
		rows = append(rows, row)
	}

	table := tablewriter.NewTable(os.Stdout)
	table.Header(headers)
	table.Bulk(rows)
	table.Render()
}

func runSingleDay(args lib.RunnerArgs) (solutions.SolutionOutput, error) {
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
		return output, err
	}

	return output, nil
}
