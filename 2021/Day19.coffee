# Definitely not an excuse to use Javascript again for a hard problem

# Scanners can detect beacons within a 1000x1000x1000 cube relative to their position
# Scanners do not detect other scanners
# Scanners do not know their own position

# Can construct 3d region based on scanners that detect overlapping beacons
# Need to detect 12 beacons that both scanners detect within an overlap
# Once that's done you can reconstruct the region

# Scanners don't know their rotation/direction
# Rotated some multiple of 90-degrees in x, y, and z.
# Could be 1 of 24 orientations

# Matrix math helper functions
sin = (theta) ->
    switch theta
        when 0 then 0
        when -270, 90 then 1
        when -180, 180 then 0
        when -90, 270 then -1

cos = (theta) ->
    switch theta
        when 0 then 1
        when -270, 90 then 0
        when -180, 180 then -1
        when -90, 270 then 0

rotMatrix = (x, y, z) ->
    [
        [
            cos(y) * cos(z),
            cos(x) * sin(z) + sin(x) * sin(y) * cos(z),
            sin(x) * sin(z) - cos(x) * sin(y) * cos(z)
        ],
        [
            -cos(y) * sin(z),
            cos(x) * cos(z) - sin(x) * sin(y) * sin(z),
            sin(x) * cos(z) + cos(x) * sin(y) * sin(z)
        ],
        [
            sin(y),
            -sin(x) * cos(y),
            cos(x) * cos(y)
        ]
    ]

printMatrix = (matrix) ->
    console.log("#{matrix[0][0]}\t#{matrix[0][1]}\t#{matrix[0][2]}")
    console.log("#{matrix[1][0]}\t#{matrix[1][1]}\t#{matrix[1][2]}")
    console.log("#{matrix[2][0]}\t#{matrix[2][1]}\t#{matrix[2][2]}")
    console.log("\n")

transformVector = (t, v) ->
    [
        t[0][0] * v[0] + t[0][1] * v[1] + t[0][2] * v[2],
        t[1][0] * v[0] + t[1][1] * v[1] + t[1][2] * v[2],
        t[2][0] * v[0] + t[2][1] * v[1] + t[2][2] * v[2]
    ]

distance = (p1, p2) ->
    Math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

manhattan_distance = (p1, p2) ->
    Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]) + Math.abs(p1[2] - p2[2])

fs = require('fs')

file = fs.readFileSync('inputs/test.in', 'utf-8')
         .split("\n\n")
         .map((block) -> block.split('\n').splice(1))

scanners = ((beacon.trimEnd()
                   .split(',')
                   .map((num) -> parseInt(num, 10)) for beacon in scanner)
                   .filter((beacon) -> beacon.length == 3) for scanner in file)

rotationMatrices = []
for x in [0, 90, 180]
    for y in [0, 90, 180]
        for z in [0, 90, 180]
            rotationMatrices.push(rotMatrix(x, y, z))

s0 = scanners[0][9]
s1 = scanners[1][0]

min_dist = 10000
console.log(rotationMatrices.length)
console.log(manhattan_distance([-500, 1000, -1500], [-1000, 1000, -1000]))
