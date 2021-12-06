use std::env;
use std::fs;
use std::process;
use std::cmp::{min,max};

fn coord_from_string(coord: &str) -> (usize, usize) {
    let mut split = coord.split(",")
        .map(|s| s.parse().unwrap());
    (split.next().unwrap(), split.next().unwrap())
}

fn count_overlaps(grid: &Vec<Vec<usize>>) -> usize {
    grid.iter()
        .map(|row| row.iter().filter(|&c| *c >= 2).count())
        .sum()
}

#[derive(Debug)]
struct Line {
    x1: usize,
    y1: usize,
    x2: usize,
    y2: usize,
    diag: bool,
}

impl Line {
    pub fn from_string(string: &str) -> Self {
        let mut coords = string.split(" -> ")
            .map(|coord| coord_from_string(coord));

        let start = coords.next().unwrap();
        let end = coords.next().unwrap();

        let (x1, y1) = (start.0, start.1);
        let (x2, y2) = (end.0, end.1);

        let xmax = max(x1, x2);
        let xmin = min(x1, x2);
        let ymin = min(y1, y2);
        let ymax = max(y1, y2);

        if x1 == x2 || y1 == y2 {
            Self { x1: xmin, y1: ymin, x2: xmax, y2: ymax, diag: false}
        } else {
            Self { x1, y1, x2, y2, diag: true }
        }
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
        .map(Line::from_string).collect();

    let max_x: usize = lines.iter().map(|l| max(l.x1, l.x2)).max().unwrap();
    let max_y: usize = lines.iter().map(|l| max(l.y1, l.y2)).max().unwrap();

    let mut grid = vec![vec![0usize; max_x + 1]; max_y + 1];

    lines.iter().filter(|l| !l.diag)
        .for_each(|line| {
            for row in line.y1..=line.y2 {
                for col in line.x1..=line.x2 {
                    grid[row][col] += 1;
                }
            }
        });

    println!("(a) Horizontal and vertical lines only: {}",
             count_overlaps(&grid));

    lines.iter().filter(|l| l.diag)
        .for_each(|line| {
            let cols: Vec<usize> = if line.x2 > line.x1 {
                (line.x1..=line.x2).collect()
            } else {
                (line.x2..=line.x1).rev().collect()
            };

            let rows: Vec<usize> = if line.y2 > line.y1 {
                (line.y1..=line.y2).collect()
            } else {
                (line.y2..=line.y1).rev().collect()
            };

            for i in 0..rows.len() {
                grid[rows[i]][cols[i]] += 1;
            }
        });

    println!("(b) All lines (including diagonal): {}", count_overlaps(&grid));
}
