package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"time"
)

func countBits(nums []string) []int {
	counts := make([]int, len(nums[0]))

	for _, num := range nums {
		for i, d := range num {
			if d == '1' {
				counts[i] += 1
			}
		}
	}

	return counts
}

func filterNums(nums []string, index int, useMostCommon bool) []string {
	newNums := make([]string, 0)
	counts := [2]int{0, 0}

	for _, num := range nums {
		if num[index] == '1' {
			counts[1] += 1
		} else {
			counts[0] += 1
		}
	}

	var commonDigit byte
	if useMostCommon {
		if counts[0] > counts[1] {
			commonDigit = '0'
		} else {
			commonDigit = '1'
		}
	} else {
		if counts[0] > counts[1] {
			commonDigit = '1'
		} else {
			commonDigit = '0'
		}
	}

	for _, num := range nums {
		if num[index] == commonDigit {
			newNums = append(newNums, num)
		}
	}

	return newNums
}

func main() {
	startTime := time.Now()

	// File input
	f, err := os.Open("inputs/Day03.in")
	if err != nil {
		log.Fatal(err)
	}

	// Java-like Scanner object that reads line by line
	scanner := bufio.NewScanner(f)
	nums := make([]string, 0)
	// Go uses "for" for all loops, so this is essentially a traditional "while" loop
	for scanner.Scan() {
		nums = append(nums, scanner.Text())
	}

	halfLen := len(nums) / 2
	bits := countBits(nums)
	gamma := 0
	epsilon := 0
	pow2 := 1
	// Convert part 1 results to decimal
	for i := len(nums[0]) - 1; i >= 0; i -= 1 {
		if bits[i] > halfLen {
			gamma += pow2
		} else if bits[i] < halfLen {
			epsilon += pow2
		}
		pow2 *= 2
	}

	oxygen := make([]string, len(nums))
	carbon := make([]string, len(nums))
	copy(oxygen, nums)
	copy(carbon, nums)
	L := len(nums[0])

	for i := 0; i < L; i += 1 {
		if len(oxygen) > 1 {
			oxygen = filterNums(oxygen, i, true)
		}
		if len(carbon) > 1 {
			carbon = filterNums(carbon, i, false)
		}
	}

	f.Close()

	// Convert part 2 results to decimal
	oDec := 0
	cDec := 0
	pow2 = 1
	for i := L - 1; i >= 0; i -= 1 {
		if oxygen[0][i] == '1' {
			oDec += pow2
		}
		if carbon[0][i] == '1' {
			cDec += pow2
		}
		pow2 *= 2
	}
	elapsed := time.Since(startTime)

	println(gamma * epsilon)
	println(oDec * cDec)
	fmt.Printf("Time: %s\n", elapsed)
}
