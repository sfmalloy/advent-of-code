function check_adjacent(r, c, heightmap)
    valid = true
    if r > 1
        valid = valid && heightmap[r-1][c] > heightmap[r][c]
    end
    if r < length(heightmap)
        valid = valid && heightmap[r+1][c] > heightmap[r][c]
    end
    if c > 1
        valid = valid && heightmap[r][c-1] > heightmap[r][c]
    end
    if c < length(heightmap[r])
        valid = valid && heightmap[r][c+1] > heightmap[r][c]
    end
    return valid
end

function flood(r, c, heightmap, seen)
    if heightmap[r][c] == 9 || (r, c) in seen
        return seen
    end

    new_seen = union(seen, Set([(r, c)]))
    if r > 1
        union!(new_seen, flood(r-1, c, heightmap, new_seen))
    end
    if r < length(heightmap)
        union!(new_seen, flood(r+1, c, heightmap, new_seen))
    end
    if c > 1
        union!(new_seen, flood(r, c-1, heightmap, new_seen))
    end
    if c < length(heightmap[r])
        union!(new_seen, flood(r, c+1, heightmap, new_seen))
    end

    return new_seen
end

function main()
    heightmap = []
    for line in eachline("inputs/Day09.in")
        push!(heightmap, map(c -> parse(Int64, c), split(line, "")))
    end

    part1 = 0
    low_points = []
    for row in 1:length(heightmap)
        for col in 1:length(heightmap[row])
            if check_adjacent(row, col, heightmap)
                part1 += 1 + heightmap[row][col]
                push!(low_points, (row, col))
            end
        end
    end
    println(part1)

    sizes = []
    for (row, col) in low_points
        push!(sizes, flood(row, col, heightmap, Set()))
    end

    sorted = sort(map(s -> length(s), sizes))
    println(sorted[length(sorted)] * sorted[length(sorted)-1] * sorted[length(sorted)-2])
end

main()
