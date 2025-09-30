package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"

	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load()
	os.Getenv("AOC_SESSION")
	file, err := readInput(2024, 1)
	if err != nil {
		fmt.Printf("Error getting input file: %s\n", err)
		os.Exit(1)
	}

	buf, err := io.ReadAll(file)
	if err != nil {
		fmt.Printf("Failed to read file %s\n", err)
		os.Exit(1)
	}

	fmt.Printf("%d\n", len(string(buf)))
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
	} else {
		fmt.Println("good")
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
	req.Header.Add("User-Agent", "email:sfmalloy.dev@gmail.com repo:https://github.com/sfmalloy/advent-of-code-{YEAR}")

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
