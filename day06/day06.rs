use std::env;
use std::fs;
use std::process;


const NEW_FISH_LIVES: u8 = 8;
const REGEN_LIVES: u8 = 6;
const DEFAULT_NUM_DAYS: u32 = 80;


fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        process::exit(1);
    }

    let num_days = if args.len() > 2 {
        args[2].parse().unwrap_or(DEFAULT_NUM_DAYS)
    } else { DEFAULT_NUM_DAYS };

    let fish_file = fs::read_to_string(&args[1]).expect("Cannot open file");

    let mut fishes: Vec<u8> = fish_file.trim().split(",")
        .map(|n| n.parse().unwrap()).collect();

    for _ in 0..num_days {
        let mut new_fish = 0usize;
        for fish in &mut fishes {
            if *fish == 0 {
                *fish = REGEN_LIVES;
                new_fish += 1;
            } else {
                *fish -= 1;
            }
        }

        if new_fish > 0 {
            fishes.extend(vec![NEW_FISH_LIVES; new_fish]);
        }
    }

    println!("After {} day(s), there are {} fish remaining",
             num_days, fishes.len());
}
