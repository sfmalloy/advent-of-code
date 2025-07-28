import * as fs from 'fs'
import { performance } from 'perf_hooks'

function getCountDiff(_pairs: Map<string, number>, _counts: Map<string, number>, rules: Map<string, string>, limit: number) {
    let pairs: Map<string, number> = new Map<string, number>(_pairs)
    let counts: Map<string, number> = new Map<string, number>(_counts)
    for (let i = 0; i < limit; ++i) {
        let temp_pairs: Map<string, number> = new Map<string, number>()
        let temp_counts: Map<string, number> = new Map<string, number>()
        for (let [pair, count] of pairs) {
            if (rules.has(pair)) {
                let p1 = pair[0] + rules.get(pair)!
                let p2 = rules.get(pair) + pair[1]!
    
                let c1 = count
                if (temp_pairs.has(p1))
                    c1 += temp_pairs.get(p1)!
                temp_pairs.set(p1, c1)
                
                let c2 = count
                if (temp_pairs.has(p2))
                    c2 += temp_pairs.get(p2)!
                temp_pairs.set(p2, c2)
        
                let temp_count = count
                if (temp_counts.has(rules.get(pair)!))
                    temp_count += temp_counts.get(rules.get(pair)!)!
                temp_counts.set(rules.get(pair)!, temp_count)
            } else {
                temp_pairs.set(pair, count)
            }
        }
        for (let [elem, count] of temp_counts) {
            if (counts.has(elem))
                counts.set(elem, counts.get(elem)! + count)
            else
                counts.set(elem, count)
        }
    
        pairs = temp_pairs
    }

    let max = 0
    for (let count of counts.values()) {
        max = count > max ? count : max;
    }

    let min = max
    for (let count of counts.values()) {
        min = count < min ? count : min;
    }

    return max - min;
}

let startTime = performance.now();

let file: string[] = fs.readFileSync('inputs/Day14.in', 'utf-8').split('\n')
let polymer: string = file[0]

let rules: Map<string, string> = new Map<string, string>()
for (let line of file.splice(1)) {
    if (line.length > 0) {
        let kv: string[] = line.split(" -> ")
        rules.set(kv[0], kv[1])
    }
}

let counts: Map<string, number> = new Map<string, number>()
for (let c of polymer) {
    if (!counts.has(c))
        counts.set(c, 0)
    counts.set(c, counts.get(c)! + 1)
}

let pairs: Map<string, number> = new Map<string, number>()
for (let i = 0; i < polymer.length - 1; ++i) {
    let pair = polymer.substr(i, 2)
    if (!pairs.has(pair))
        pairs.set(pair, 0)
    pairs.set(pair, pairs.get(pair)! + 1)
}

let part1: number = getCountDiff(pairs, counts, rules, 10)
let part2: number = getCountDiff(pairs, counts, rules, 40)

let endTime = performance.now();

console.log(part1)
console.log(part2)
console.log(`Time: ${(endTime - startTime).toFixed(3)}ms`)
