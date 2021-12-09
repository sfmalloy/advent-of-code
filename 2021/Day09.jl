function checkAdjacent(r, c, heightmap)
    
end

heightmap = []
for line in eachline("inputs/Day09.in")
    push!(heightmap, map(c -> parse(Int64, c), split(line, "")))
end

for row in heightmap
    println(row)
end
