function get_start_pos(str)
    local _, b = string.find(str, ": ")
    return string.sub(str, b+1)
end

function simulate_deterministic(die, pos)
    local roll = 3*die + 3
    pos = pos + roll
    while pos > 10 do
        pos = pos - 10
    end
    return pos
end

function simulate_dirac(curr_pos, added)
    pos = curr_pos + added
    while pos > 10 do
        return pos - 10
    end
    return pos
end

cache = {}
function dirac(player, pos1, pos2, score1, score2)
    local hash = player ~ (pos1 << 4) ~ (pos2 << 8) ~ (score1 << 16) ~ (score2 << 24)
    if cache[hash] then
        return cache[hash]
    end

    if player == 2 and score1 >= 21 then
        cache[hash] = { 1, 0 }
    elseif player == 1 and score2 >= 21 then
        cache[hash] = { 0, 1 }
    else
        local p1 = 0
        local p2 = 0
        if player == 1 then
            for i=1,3 do
                for j=1,3 do
                    for k=1,3 do
                        local roll = i+j+k
                        local next_pos = simulate_dirac(pos1, roll)
                        local res = dirac(2, next_pos, pos2, score1+next_pos, score2)
                        p1 = p1 + res[1]
                        p2 = p2 + res[2]
                    end
                end
            end
        else
            for i=1,3 do
                for j=1,3 do
                    for k=1,3 do
                        local roll = i+j+k
                        local next_pos = simulate_dirac(pos2, roll)
                        local res = dirac(1, pos1, next_pos, score1, score2+next_pos)
                        p1 = p1 + res[1]
                        p2 = p2 + res[2]
                    end
                end
            end
        end
        cache[hash] = { p1, p2 }
    end

    return cache[hash]
end

function main()
    local filename = "inputs/Day21.in"
    local file = io.open(filename, "r")
    io.input(file)

    local p1 = get_start_pos(io.read())
    local p2 = get_start_pos(io.read())

    local pos1 = p1
    local pos2 = p2

    local score1 = 0
    local score2 = 0
    local die = 1
    local turn = 1

    while score1 < 1000 and score2 < 1000 do
        pos1 = simulate_deterministic(die, pos1)
        score1 = score1 + pos1
        die = die + 3
        turn = turn + 1

        if score1 < 1000 then
            pos2 = simulate_deterministic(die, pos2)
            score2 = score2 + pos2
            die = die + 3
            turn = turn + 1
        end
    end

    local part1
    if score1 > score2 then
        part1 = score2 * (die - 1)
    else
        part1 = score1 * (die - 1)
    end

    local part2
    t = dirac(1, tonumber(p1), tonumber(p2), 0, 0)
    if t[1] > t[2] then
        part2 = t[1]
    else
        part2 = t[2]
    end

    print(part1)
    print(part2)
end

main()
