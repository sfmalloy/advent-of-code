let intersection = (a, b) => {
    let intersect = new Set();
    for (let elem of b) {
        if (a.has(elem)) {
            intersect.add(elem);
        }
    }
    return intersect;
}

let negation = (fullset, subset) => {
    let negate = new Set();
    for (let elem of fullset) {
        if (!subset.has(elem)) {
            negate.add(elem);
        }
    }

    return negate;
}

let findPattern = (number, keys, others, compareFunction) => {
    let removeIndex = -1;
    for (let pattern of others) {
        if (compareFunction(keys, pattern)) {
            keys[number] = pattern;
            removeIndex = others.indexOf(pattern);
            break;
        }
    }
    others.splice(removeIndex, 1);
}

let startTime = performance.now();

let fs = require('fs');
let file = fs.readFileSync('inputs/Day08.in', 'utf-8');
let entries = file.split('\n').map((s) => {
    let pair = s.split('|');
    if (pair.length > 1) {
        pair[0] = pair[0].split(' ').slice(0, -1);
        pair[1] = pair[1].split(' ').slice(1);
    }
    return pair;
});
entries.pop();

let easyCount = 0;
let easyLengths = new Map();
easyLengths.set(2, 1);
easyLengths.set(3, 7);
easyLengths.set(4, 4);
easyLengths.set(7, 8);

for (let i = 0; i < entries.length; ++i) {
    for (let output of entries[i][1]) {
        if (easyLengths.has(output.length)) {
            ++easyCount;
        }
    }
}

let sum = 0;
for (let entry of entries) {
    let keys = {};
    let others = [];
    // Find 1,7,4,8 and filter out the rest
    for (let signal of entry[0]) {
        let pattern = new Set(signal.split(''));
        if (easyLengths.has(signal.length)) {
            keys[easyLengths.get(signal.length)] = pattern;
        } else {
            others.push(pattern);
        }
    }

    // Use different combinations of intersections and negations to filter the rest
    // of the cases.
    findPattern(9, keys, others, (keys, pattern) => {
        return intersection(keys[4], pattern).size == 4;
    });

    findPattern(0, keys, others, (keys, pattern) => {
        let negate = negation(keys[8], pattern);
        return negate.size == 1 && intersection(negate, keys[1]).size == 0;
    });

    findPattern(6, keys, others, (keys, pattern) => {
        return pattern.size == 6;
    });

    findPattern(3, keys, others, (keys, pattern) => {
        return intersection(keys[1], pattern).size == 2;
    });

    findPattern(5, keys, others, (keys, pattern) => {
        return intersection(keys[6], pattern).size == 5;
    });

    keys[2] = others[0];

    let num = '';
    for (let digit of entry[1]) {
        let signalSet = new Set(digit.split(''));
        for (let i = 0; i < 10; ++i) {
            if (keys[i].size == signalSet.size && intersection(keys[i], signalSet).size == keys[i].size) {
                num += '' + i;
            }
        }
    }

    sum += parseInt(num);
}

let endTime = performance.now();

console.log(easyCount);
console.log(sum);
console.log(`Time: ${(endTime - startTime).toFixed(3)}ms`)
