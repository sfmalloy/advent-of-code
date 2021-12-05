def bounds(a, b)
    start = 0
    finish = 0
    if a < b then
        return a, b
    end
    return b, a
end

Point = Struct.new(:x, :y)

no_diag = Hash.new(0)
diag = Hash.new(0)

File.readlines("inputs/Day05.in").each do |line|
    p1, p2 = line.split(" -> ")
    x1, y1 = p1.split(",").map(&:to_i)
    x2, y2 = p2.split(",").map(&:to_i)

    dx = 0
    dy = 0
    x = x_end = y = y_end = 0
    is_diag = false
    if y1 == y2 then
        dx = 1
        y = y_end = y1
        x, x_end = bounds(x1, x2)
    elsif x1 == x2 then
        dy = 1
        x = x_end = x1
        y, y_end = bounds(y1, y2)
    elsif x1 > x2 then
        dy = y2 < y1 ? 1 : -1
        dx = 1
        x = x2
        y = y2
        x_end = x1
        y_end = y1
        is_diag = true
    else
        dy = y1 < y2 ? 1 : -1
        dx = 1
        x = x1
        y = y1
        x_end = x2
        y_end = y1
        is_diag = true
    end

    if not is_diag then
        while x <= x_end and y <= y_end do
            pt = Point.new(x, y)
            no_diag[pt] += 1
            diag[pt] += 1
            y += dy
            x += dx
        end
    else
        while x <= x_end do
            pt = Point.new(x, y)
            diag[pt] += 1
            y += dy
            x += dx
        end
    end
end

part1 = 0
no_diag.each do |pt, count|
    if count > 1 then
        part1 += 1
    end
end
puts part1

part2 = 0
diag.each do |pt, count|
    if count > 1 then
        part2 += 1
    end
end
puts part2
