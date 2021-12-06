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

struct Line {
    x1: usize,
    y1: usize,
    x2: usize,
    y2: usize,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        process::exit(1);
    }

    let lines_file = fs::read_to_string(&args[1])
        .expect("Cannot open file");

    let mut max_x = 0usize;
    let mut max_y = 0usize;
    let lines: Vec<Line> = lines_file.lines()
        .map(|line| {
            let mut coords = line.split(" -> ")
                .map(|coord| coord_from_string(coord));

            let start = coords.next().unwrap();
            let end = coords.next().unwrap();

            let xmax = max(start.0, end.0);
            let xmin = min(start.0, end.0);
            let ymin = min(start.1, end.1);
            let ymax = max(start.1, end.1);

            max_x = max(max_x, xmax);
            max_y = max(max_y, ymax);

            Line { x1: xmin, y1: ymin, x2: xmax, y2: ymax }
        }).collect();

    let hor_ver_lines: Vec<&Line> = lines.iter()
        .filter(|&l| (l.x1 == l.x2) || (l.y1 == l.y2))
        .collect();

    let mut grid_hor_ver = vec![vec![0usize; max_x + 1]; max_y + 1];
    for line in hor_ver_lines {
        for row in line.y1..=line.y2 {
            for col in line.x1..=line.x2 {
                grid_hor_ver[row][col] += 1;
            }
        }
    }

    println!("Horizontal and vertical lines only: {}",
             count_overlaps(&grid_hor_ver));
}
