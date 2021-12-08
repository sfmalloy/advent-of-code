/*jshint esversion: 6 */

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

let part1 = 0;
let easy_lengths = [2,3,4,7];
for (let i = 0; i < entries.length; ++i) {
    for (let output of entries[i][1]) {
        if (easy_lengths.includes(output.length)) {
            ++part1;
        }
    }
}

console.log(part1);

// Start of part 2
// for (let entry in entries) {
//     let keys = new Map();
//     for (let signal in entry[1]) {
//         if (signal.length == 2)
//             keys.set(1, signal);
//         else if (signal.length == 3)
//             keys.set(7, signal);
//         else if (signal.length == 9)
//     }
// }
