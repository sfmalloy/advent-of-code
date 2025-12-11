package solutions

import (
	"io"
	"os"
	"strings"
)

type Day11 struct{}

func (d Day11) Parse(file *os.File, part int) (map[string][]string, error) {
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}
	servers := map[string][]string{}
	for line := range strings.Lines(string(data)) {
		line = strings.Trim(line, "\n")
		parts := strings.Split(line, ": ")
		key := parts[0]
		servers[key] = []string{}
		for val := range strings.SplitSeq(parts[1], " ") {
			servers[key] = append(servers[key], val)
		}
	}
	return servers, nil
}

func (d Day11) Part1(servers map[string][]string) int {
	return follow1("you", 0, servers)
}

func (d Day11) Part2(servers map[string][]string) int {
	cache := map[string]int{}
	return follow2("svr", false, false, servers, cache)
}

func follow1(server string, total int, servers map[string][]string) int {
	if server == "out" {
		return total + 1
	}
	for _, output := range servers[server] {
		total = follow1(output, total, servers)
	}
	return total
}

func follow2(server string, fft, dac bool, servers map[string][]string, cache map[string]int) int {
	key := server + boolKey(fft) + boolKey(dac)
	if val, ok := cache[key]; ok {
		return val
	}
	if server == "out" {
		if fft && dac {
			return 1
		} else {
			return 0
		}
	}
	total := 0
	for _, output := range servers[server] {
		total += follow2(
			output,
			fft || output == "fft",
			dac || output == "dac",
			servers,
			cache,
		)
	}
	cache[key] = total
	return cache[key]
}

func boolKey(b bool) string {
	if b {
		return "1"
	}
	return "0"
}
