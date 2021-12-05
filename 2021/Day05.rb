Point = Struct.new(:x, :y)

part1 = Hash.new
points = Hash.new
File.readlines("inputs/Day05.in").each do |line|
    p1, p2 = line.split(" -> ")
    x1, y1 = p1.split(",").map(&:to_i)
    x2, y2 = p2.split(",").map(&:to_i)
    if y1 == y2 then
        start = x1 < x2 ? x1 : x2
        finish = x1 == start ? x2 : x1
        for x in start..finish do
            pt = Point.new(x, y1)
            if not points.has_key?(pt) then
                points[pt] = 0
            end
            if not part1.has_key?(pt) then
                part1[pt] = 0
            end
            part1[pt] += 1
            points[pt] += 1
        end
    elsif x1 == x2 then
        start = y1 < y2 ? y1 : y2
        finish = y1 == start ? y2 : y1
        for y in start..finish do
            pt = Point.new(x1, y)
            if not points.has_key?(pt) then
                points[pt] = 0
            end
            if not part1.has_key?(pt) then
                part1[pt] = 0
            end
            part1[pt] += 1
            points[pt] += 1
        end
    elsif x1 > x2 then
        dy = y2 < y1 ? 1 : -1
        x = x2
        y = y2
        while x <= x1 do
            pt = Point.new(x, y)
            if not points.has_key?(pt) then
                points[pt] = 0
            end
            points[pt] += 1
            x += 1
            y += dy
        end
    elsif x2 > x1 then
        dy = y1 < y2 ? 1 : -1
        x = x1
        y = y1
        while x <= x2 do
            pt = Point.new(x, y)
            if not points.has_key?(pt) then
                points[pt] = 0
            end
            points[pt] += 1
            x += 1
            y += dy
        end
    end
end

total = 0
part1.each do |pt, count|
    if count > 1 then
        total += 1
    end
end
puts total

total = 0
points.each do |pt, count|
    if count > 1 then
        total += 1
    end
end

puts total
