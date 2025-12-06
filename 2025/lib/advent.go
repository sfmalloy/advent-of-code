package lib

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

func DownloadInput(year int, day int) error {
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
