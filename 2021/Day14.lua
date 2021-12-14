function Split(str)
    local a, b = string.find(str, " -> ")
    return string.sub(str, 1, a-3), string.sub(str, b+1)
end

local filename = "inputs/Day14.in"
local file = io.open(filename, "r")
io.input(file)

local polymer = nil
local rules = {}
for l in io.lines(filename) do
    if (string.len(l) > 0) then
        if (polymer == nil) then
            polymer = l
        else
            table.insert(rules, l)
            local key, value = Split(l)
            rules[key] = value
        end
    end
end

for k=1,40 do
    local new_polymer = ""
    for i=1,string.len(polymer)-1 do
        local first = string.sub(polymer, i, i)
        local second = string.sub(polymer, i+1, i+1)
        local pair = first .. second
        if (rules[pair] ~= nil) then
            new_polymer = new_polymer .. first .. rules[pair]
        else
            new_polymer = new_polymer .. first
        end
    end
    polymer = new_polymer .. string.sub(polymer, #polymer)
end

local counts = {}
for elem in polymer:gmatch(".") do
    if (counts[elem] ~= nil) then
        counts[elem] = counts[elem] + 1
    else
        counts[elem] = 0
    end
end

local mx = 0
local mn = 1000000000000
for _, count in pairs(counts) do
    if mx < count then
        mx = count
    elseif mn > count then
        mn = count
    end
end

print(mx-mn)
