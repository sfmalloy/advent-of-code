package main

import (
	"bufio"
	"log"
	"os"
)

const BUFFER = 12

func binToDec(bin string) int {
	res := 0
	pow2 := 1

	for i := len(bin) - 1; i >= 0; i -= 1 {
		res += pow2 * (int(bin[i]) - int('0'))
		pow2 *= 2
	}

	return res
}

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
	f, err := os.Open("inputs/Day03.in")
	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)
	nums := make([]string, 0)

	// equivalent to while scanner.hasNext() like in Java
	for scanner.Scan() {
		nums = append(nums, scanner.Text())
	}

	bits := countBits(nums)
	gamma := 0
	epsilon := 0
	pow2 := 1
	numLines := len(nums)
	for i := len(nums[0]) - 1; i >= 0; i -= 1 {
		if bits[i] > numLines/2 {
			gamma += pow2
		} else if bits[i] < numLines/2 {
			epsilon += pow2
		}
		pow2 *= 2
	}

	// Part 1
	println(gamma * epsilon)

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

	// Part 2
	println(binToDec(oxygen[0]) * binToDec(carbon[0]))
}
