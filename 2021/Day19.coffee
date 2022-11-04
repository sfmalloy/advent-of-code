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

transformVector = (t, v) ->
    [
        t[0][0] * v[0] + t[0][1] * v[1] + t[0][2] * v[2],
        t[1][0] * v[0] + t[1][1] * v[1] + t[1][2] * v[2],
        t[2][0] * v[0] + t[2][1] * v[1] + t[2][2] * v[2]
    ]

vecDiff = (lhs, rhs) ->
    [lhs[0] - rhs[0], lhs[1] - rhs[1], lhs[2] - rhs[2]]

vecAdd = (lhs, rhs) ->
    [lhs[0] + rhs[0], lhs[1] + rhs[1], lhs[2] + rhs[2]]

vecEqual = (a, b) ->
    a[0] == b[0] && a[1] == b[1] && a[2] == b[2]

startTime = performance.now()

rotationMatrices = []
for x in [0, 90, 180, 270]
    for y in [0, 90, 180, 270]
        for z in [0, 90, 180, 270]
            eq = false
            curr = rotMatrix(x, y, z)
            for m in rotationMatrices
                if vecEqual(m[0], curr[0]) \
                    && vecEqual(m[1], curr[1]) \
                    && vecEqual(m[2], curr[2])
                    eq = true
                    break
            if !eq
                rotationMatrices.push(curr)

getDiff = (root, t, scanners) ->
    diffs = {}
    for a in scanners[root]
        for b in scanners[t]
            for m in rotationMatrices
                diff = vecDiff(a, transformVector(m, b))
                if !vecEqual(diff, [0, 0, 0])
                    strDiff = JSON.stringify([diff, root, t, m])
                    if !(strDiff of diffs)
                        diffs[strDiff] = []
                    diffs[strDiff].push([a, transformVector(m, b)])
    return diffs


findBeacons = (root, scanners) ->
    diffs = {}
    for t in [0..scanners.length - 1]
        diff = getDiff(root, t, scanners)
        diffs = { ...diffs, ...diff }
    beacons = {}
    for d, a of diffs
        if a.length >= 12
            beacons[d] = a
    return beacons

manhattanDistance = (p1, p2) ->
    Math.abs(p1[0] - p2[0]) + Math.abs(p1[1] - p2[1]) + Math.abs(p1[2] - p2[2])

console.log('THIS WILL TAKE AWHILE')
file = require('fs').readFileSync('inputs/Day19.in', 'utf-8')
         .split("\n\n")
         .map((block) -> block.split('\n').splice(1))

scanners = ((beacon.trimEnd()
                   .split(',')
                   .map((num) -> parseInt(num, 10)) for beacon in scanner)
                   .filter((beacon) -> beacon.length == 3) for scanner in file)

positions = {
    0: [0, 0, 0]
}

rotations = {
    0: -1
}

done = new Set()
next = [0]
while next.length > 0
    curr = next.shift()
    beaconMap = findBeacons(curr, scanners)
    if !done.has(curr)
        for key, beaconList of beaconMap
            [diff, start, end, rot] = JSON.parse(key)
            if start of positions
                rotations[end] = m
                for i in [0..scanners[end].length - 1]
                    scanners[end][i] = transformVector(rot, scanners[end][i])
                positions[end] = vecAdd(diff, positions[start])
            if !done.has(end) && !next.includes(end)
                next.push(end)
        done.add(curr)
    if done.size == Math.floor(scanners.length / 2)
        console.log('Still going...')

unique = new Set
largestDist = 0
for s in [0..scanners.length - 1]
    scn = scanners[s]
    for p in [0..scn.length - 1]
        unique.add(JSON.stringify(vecAdd(positions[s], scn[p])))
    for t in [s..scanners.length - 1]
        largestDist = Math.max(largestDist, manhattanDistance(positions[s], positions[t]))

console.log(unique.size)
console.log(largestDist)

endTime = performance.now()

minutes = Math.floor(((endTime - startTime) / 1000) / 60)
seconds = Math.round(((endTime - startTime) / 1000) - (minutes * 60))

console.log("Time: #{minutes}min #{seconds}sec")
