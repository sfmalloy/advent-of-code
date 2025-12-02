package main

import (
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
	"github.com/sfmalloy/advent-of-code/2025/solutions"
)

type RunnerArgs struct {
	Day       int
	Part      int
	InputFile string
}

func main() {
	godotenv.Load()
	os.Getenv("AOC_SESSION")
	args := parseArgs()

	switch args.Day {
	case 1:
		runHandler(solutions.Day01{}, args)
	case 2:
		runHandler(solutions.Day02{}, args)
	case 3:
		runHandler(solutions.Day03{}, args)
	case 4:
		runHandler(solutions.Day04{}, args)
	case 5:
		runHandler(solutions.Day05{}, args)
	case 6:
		runHandler(solutions.Day06{}, args)
	case 7:
		runHandler(solutions.Day07{}, args)
	case 8:
		runHandler(solutions.Day08{}, args)
	case 9:
		runHandler(solutions.Day09{}, args)
	case 10:
		runHandler(solutions.Day10{}, args)
	case 11:
		runHandler(solutions.Day11{}, args)
	case 12:
		runHandler(solutions.Day12{}, args)
	default:
		fmt.Printf("Invalid day: %d\n", args.Day)
		os.Exit(1)
	}
}

func runHandler[I any, O any](day solutions.Day[I, O], args RunnerArgs) {
	totalTime := 0.0
	runBoth := args.Part == 0
	if args.Part == 1 || runBoth {
		args.Part = 1
		time, output, err := runDay(day, args)
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		totalTime += time
		fmt.Printf("Part 1: %v\n", *output)
	}
	if args.Part == 2 || runBoth {
		args.Part = 2
		time, output, err := runDay(day, args)
		if err != nil {
			fmt.Println(err.Error())
			return
		}
		totalTime += time
		fmt.Printf("Part 2: %v\n", *output)
	}

	fmt.Printf("Time: %.03fms\n", totalTime)
}

func runDay[I any, O any](day solutions.Day[I, O], args RunnerArgs) (float64, *O, error) {
	year, err := strconv.ParseInt(os.Getenv("AOC_YEAR"), 10, 32)
	year32 := int32(year)
	if err != nil {
		return 0, nil, fmt.Errorf("Invaild year")
	}
	input, err := getInputFile(args, int(year32))
	if err != nil {
		return 0, nil, err
	}

	parsed, err := day.Parse(input)
	if err != nil {
		return 0, nil, err
	}

	if args.Part == 1 {
		time, out := runPart(parsed, day.Part1)
		return time, &out, nil
	}
	if args.Part == 2 {
		time, out := runPart(parsed, day.Part2)
		return time, &out, nil
	}

	return 0, nil, fmt.Errorf("Invalid part number")
}

func runPart[I any, O any](input I, fn func(I) O) (float64, O) {
	startTime := time.Now()
	output := fn(input)
	endTime := float64(time.Since(startTime).Microseconds()) / 1000
	return endTime, output
}

func getInputFile(args RunnerArgs, year int) (*os.File, error) {
	if len(args.InputFile) == 0 {
		return readInput(year, args.Day)
	}
	file, err := os.Open(args.InputFile)
	if err != nil {
		return nil, err
	}
	return file, nil
}

func readInput(year int, day int) (*os.File, error) {
	filepath := fmt.Sprintf("inputs/day%02d.txt", day)
	file, err := os.Open(filepath)
	if errors.Is(err, os.ErrNotExist) {
		fmt.Println("Downloading input...")
		err = downloadInput(year, day)
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

func downloadInput(year int, day int) error {
	// Validate that we aren't too soon to download today's input
	// Puzzles release at midnight EST so we check that
	est, err := time.LoadLocation("America/New_York")
	if err != nil {
		return err
	}
	if time.Until(time.Date(year, time.December, day, 0, 0, 0, 0, est)) > 0 {
		return fmt.Errorf("Too soon to download day %d", day)
	}
	err = limitRequestTime()
	if err != nil {
		return err
	}

	// Construct and send request to API
	client := http.Client{}
	req, err := http.NewRequest("GET", fmt.Sprintf("https://adventofcode.com/%d/day/%d/input", year, day), nil)
	if err != nil {
		return err
	}
	auth := http.Cookie{
		Name:  "session",
		Value: os.Getenv("AOC_SESSION"),
	}
	req.AddCookie(&auth)
	req.Header.Add("User-Agent", "email:sfmalloy.dev@gmail.com repo:https://github.com/sfmalloy/advent-of-code")

	res, err := client.Do(req)
	if err != nil {
		return err
	} else if res.StatusCode != 200 {
		return fmt.Errorf("HTTP error calling AOC: %d (%s)", res.StatusCode, res.Status)
	}

	// Write downloaded input to file
	defer res.Body.Close()
	data, err := io.ReadAll(res.Body)
	if err != nil {
		return err
	}

	file, err := os.Create(fmt.Sprintf("inputs/day%02d.txt", day))
	if err != nil {
		return err
	}
	file.Write(data)
	file.Close()

	return nil
}

func parseArgs() RunnerArgs {
	var args = RunnerArgs{}
	isTest := false
	flag.BoolVar(&isTest, "t", false, "Shorthand for -f inputs/test.txt")
	flag.IntVar(&args.Day, "d", 0, "Day to run")
	flag.IntVar(&args.Part, "p", 0, "Part of this day to run")
	flag.StringVar(&args.InputFile, "f", "", "Path to input file")
	flag.Parse()

	if isTest {
		args.InputFile = "inputs/test.txt"
	}
	return args
}

func limitRequestTime() error {
	const filename = "inputs/.last-request-time.txt"
	fileContent, err := os.ReadFile(filename)
	if os.IsNotExist(err) {
		file, err := os.Create("inputs/.last-request-time.txt")
		timestamp, err := time.Now().MarshalText()
		if err != nil {
			return err
		}
		file.Write(timestamp)
		file.Close()
		return nil
	}

	timestamp, err := time.Parse(time.RFC3339, string(fileContent))
	if time.Since(timestamp) < 15*time.Minute {
		return fmt.Errorf("Must wait 15 minutes until next download request")
	}
	newTimestamp, err := time.Now().MarshalText()
	if err != nil {
		return err
	}
	err = os.WriteFile(filename, newTimestamp, 0o644) // -rw-r--r--
	if err != nil {
		return err
	}

	return nil
}
