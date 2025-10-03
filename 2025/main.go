package main

import (
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/joho/godotenv"
	"github.com/sfmalloy/advent-of-code/2025/solutions"
)

type RunnerArgs struct {
	Day       int
	Part      int
	InputFile string
}

const YEAR = 2025

func main() {
	godotenv.Load()
	os.Getenv("AOC_SESSION")
	args := parseArgs()

	switch args.Day {
	case 1:
		runDay(solutions.Day01{}, args)
	case 2:
		runDay(solutions.Day02{}, args)
	case 3:
		runDay(solutions.Day03{}, args)
	case 4:
		runDay(solutions.Day04{}, args)
	case 5:
		runDay(solutions.Day05{}, args)
	case 6:
		runDay(solutions.Day06{}, args)
	case 7:
		runDay(solutions.Day07{}, args)
	case 8:
		runDay(solutions.Day08{}, args)
	case 9:
		runDay(solutions.Day09{}, args)
	case 10:
		runDay(solutions.Day10{}, args)
	case 11:
		runDay(solutions.Day11{}, args)
	case 12:
		runDay(solutions.Day12{}, args)
	case 13:
		runDay(solutions.Day13{}, args)
	case 14:
		runDay(solutions.Day14{}, args)
	case 15:
		runDay(solutions.Day15{}, args)
	case 16:
		runDay(solutions.Day16{}, args)
	case 17:
		runDay(solutions.Day17{}, args)
	case 18:
		runDay(solutions.Day18{}, args)
	case 19:
		runDay(solutions.Day19{}, args)
	case 20:
		runDay(solutions.Day20{}, args)
	case 21:
		runDay(solutions.Day21{}, args)
	case 22:
		runDay(solutions.Day22{}, args)
	case 23:
		runDay(solutions.Day23{}, args)
	case 24:
		runDay(solutions.Day24{}, args)
	case 25:
		runDay(solutions.Day25{}, args)
	default:
		fmt.Printf("Invalid day: %d\n", args.Day)
		os.Exit(1)
	}
}

func runDay[I any, O any](day solutions.Day[I, O], args RunnerArgs) error {
	input, err := getInputFile(args, YEAR)
	if err != nil {
		fmt.Printf("Error reading input file: %s\n", err)
		os.Exit(1)
	}

	parsed, err := day.Parse(input)
	if err != nil {
		return fmt.Errorf("Error parsing input file")
	}

	if args.Part == 1 || args.Part == 0 {
		fmt.Println(day.Part1(parsed))
	}
	if args.Part == 2 || args.Part == 0 {
		fmt.Println(day.Part2(parsed))
	}

	return nil
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
