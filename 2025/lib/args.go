package lib

import "flag"

type RunnerArgs struct {
	Day       int
	Part      int
	InputFile string
	NumRuns   int
}

func ParseArgs() RunnerArgs {
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
