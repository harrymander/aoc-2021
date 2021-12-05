use std::env;
use std::fs;
use std::process;

struct Grid {
    nums: Vec<Vec<u32>>,
    matches: Vec<Vec<bool>>,
}

impl Grid {
    pub fn new(bingo: &str) -> Self {
        let nums: Vec<Vec<u32>> = bingo.lines().map(|row|
            row.split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect()
        ).collect();

        let matches = vec![vec![false; nums[0].len()]; nums.len()];
        Self { nums, matches }
    }

    pub fn add_number(&mut self, number: u32) -> bool {
        let mut matched = false;
        for (i, row) in self.nums.iter().enumerate() {
            for (j, num) in row.iter().enumerate() {
                if number == *num {
                    matched = true;
                    self.matches[i][j] = true;
                }
            }
        }

        matched
    }

    pub fn sum_unmarked(&self) -> u32 {
        let mut sum = 0;
        for (i, row) in self.nums.iter().enumerate() {
            for (j, num) in row.iter().enumerate() {
                if !self.matches[i][j] {
                    sum += *num;
                }
            }
        }

        sum
    }

    pub fn is_win(&self) -> bool {
        let row_win = self.matches.iter().any(|row|
            row.iter().all(|m| *m)
        );

        let col_win = (0..self.matches[0].len()).any(|i|
            self.matches.iter().all(|row| row[i])
        );

        row_win || col_win
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        process::exit(1);
    }

    let bingo_file = fs::read_to_string(&args[1])
        .expect("Cannot open file");

    let mut segment_splits = bingo_file.split("\n\n");

    let draws: Vec<u32> = segment_splits.next().unwrap()
        .split(",")
        .map(|s| s.parse().unwrap())
        .collect();

    let mut grids: Vec<Grid> = segment_splits.map(|seg| Grid::new(seg)).collect();

    let mut won = vec![false; grids.len()];
    let mut first_winner = 0;
    let mut last_winner = 0;
    for number in draws {
        for (i, grid) in grids.iter_mut().enumerate() {
            if !won[i] {
                grid.add_number(number);
                if grid.is_win() {
                    let score = grid.sum_unmarked() * number;
                    if first_winner == 0 {
                        first_winner = score;
                    }
                    last_winner = score;
                    won[i] = true;
                }
            }
        }
    }

    println!("First winning score: {}, last winning score: {}",
             first_winner, last_winner);
}
