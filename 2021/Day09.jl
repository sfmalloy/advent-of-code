function check_adjacent(r::Int64, c::Int64, heightmap::Vector{Vector{Int64}})::Bool
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

function flood(r::Int64, c::Int64, heightmap::Vector{Vector{Int64}}, seen::BitSet)::BitSet
    if heightmap[r][c] == 9 || (r * length(heightmap[r]) + c) in seen
        return seen
    end

    push!(seen, (r * length(heightmap[r]) + c))
    if r > 1
        union!(seen, flood(r-1, c, heightmap, seen))
    end
    if r < length(heightmap)
        union!(seen, flood(r+1, c, heightmap, seen))
    end
    if c > 1
        union!(seen, flood(r, c-1, heightmap, seen))
    end
    if c < length(heightmap[r])
        union!(seen, flood(r, c+1, heightmap, seen))
    end

    return seen
end

function main()
    heightmap = Vector{Int64}[]
    for line in eachline("inputs/Day09.in")
        push!(heightmap, map(c -> parse(Int64, c), split(line, "")))
    end

    part1 = 0
    low_points = Tuple{Int64,Int64}[]
    for row in 1:length(heightmap)
        for col in 1:length(heightmap[row])
            if check_adjacent(row, col, heightmap)
                part1 += 1 + heightmap[row][col]
                push!(low_points, (row, col))
            end
        end
    end

    sizes = Int64[]
    for (row, col) in low_points
        push!(sizes, length(flood(row, col, heightmap, BitSet())))
    end

    sort!(sizes)
    part2 = sizes[length(sizes)] * sizes[length(sizes)-1] * sizes[length(sizes)-2]

    println(part1)
    println(part2)
end

main()
