use std::env;
use std::fs;
use std::process;

#[derive(Debug)]
struct Coord {
    x: u32,
    y: u32
}

#[derive(Debug)]
struct Line {
    start: Coord,
    end: Coord,
}

impl Coord {
    pub fn from_string(string: &str) -> Self {
        let mut split = string.split(",")
            .map(|s| s.trim().parse().unwrap());
        Self { x: split.next().unwrap(), y: split.next().unwrap() }
    }
}

impl Line {
    pub fn from_string(string: &str) -> Self {
        let mut split = string.split("->")
            .map(|s| Coord::from_string(s));
        Self { start: split.next().unwrap(), end: split.next().unwrap() }
    }

    pub fn overlaps(&self, line: &Line) -> u32 {
        0
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        process::exit(1);
    }

    let lines_file = fs::read_to_string(&args[1])
        .expect("Cannot open file");

    let lines: Vec<Line> = lines_file.lines()
        .map(|line| Line::from_string(line)).collect();

    let mut overlaps: u32 = 0;
    for i in 0..(lines.len() - 1) {
        for j in (i + 1)..lines.len() {
            overlaps += lines[i].overlaps(&lines[j]);
        }
    }

    println!("{}", overlaps);
}
