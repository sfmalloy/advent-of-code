use std::cmp;
use std::fs;
use std::vec::Vec;
use std::collections::HashSet;
use std::time::Instant;

#[derive(Eq, Hash, PartialEq, Copy, Clone)]
struct Point {
    x: i32,
    y: i32
}

fn main() {
    let start_time = Instant::now();

    let file_contents: String = fs::read_to_string("inputs/Day13.in").expect("Input file not found");
    let lines: Vec<&str> = file_contents.split('\n').collect();
    let mut points: HashSet<Point> = HashSet::new();
    let mut folds: Vec<Point> = Vec::new();

    for l in &lines {
        if l.len() > 0 {
            if l.get(..1) != Some("f") {
                let nums: Vec<&str> = l.split(",").collect();
                points.insert(Point {
                    x: nums[0].parse::<i32>().unwrap(),
                    y: nums[1].parse::<i32>().unwrap()
                });
            } else {
                let fold: Vec<&str> = l.split("=").collect();
                if fold[0].ends_with("x") {
                    folds.push(Point { x: fold[1].parse::<i32>().unwrap(), y: 0 });
                } else {
                    folds.push(Point { x: 0, y: fold[1].parse::<i32>().unwrap() });
                }
            }
        }
    }

    let first_fold = do_fold(folds[0], &points);

    for f in folds {
        points = do_fold(f, &points);
    }

    let mut max_x: i32 = 0;
    for pt in &points {
        max_x = cmp::max(pt.x, max_x);
    }

    let mut max_y: i32 = 0;
    for pt in &points {
        max_y = cmp::max(pt.y, max_y);
    }

    let mut letters: String = "".to_owned();
    for y in 0..max_y+1 {
        for x in 0..max_x+1 {
            if points.contains(&Point {x: x, y: y}) {
                letters.push_str("█");
            } else {
                letters.push_str(" ");
            }
        }
        letters.push_str("\n");
    }

    let end_time = Instant::now();

    println!("{}", first_fold.len());
    print!("{}\n", letters);
    println!("Time: {:?}", end_time.duration_since(start_time));
}

fn do_fold(fold: Point, points: &HashSet<Point>) -> HashSet<Point> {
    let mut folded: HashSet<Point> = HashSet::new();

    if fold.x > 0 {
        for pt in points {
            if pt.x > fold.x {
                folded.insert(Point { x: 2 * fold.x - pt.x, y: pt.y });
            } else {
                folded.insert(*pt);
            }
        }
    } else {
        for pt in points {
            if pt.y > fold.y {
                folded.insert(Point { x: pt.x, y: 2 * fold.y - pt.y });
            } else {
                folded.insert(*pt);
            }
        }
    }

    return folded;
}
