const NEW_FISH_LIVES: usize = 8;
const REGEN_LIVES: usize = 6;
const NUM_DAYS: usize = 256;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        std::process::exit(1);
    }

    let fish_file = std::fs::read_to_string(&args[1])
        .expect("Cannot open file");

    let fishes: Vec<u8> = fish_file.trim().split(",")
        .map(|n| n.parse().unwrap()).collect();

    let mut populations = vec![0usize; 1 + NEW_FISH_LIVES as usize];
    for fish in fishes.iter() {
        populations[*fish as usize] += 1;
    }

    let mut total_pop = fishes.len();
    for day in 1..=NUM_DAYS {
        populations.rotate_left(1);
        populations[REGEN_LIVES] += populations[NEW_FISH_LIVES];
        total_pop += populations[NEW_FISH_LIVES];

        if day == 80 || day == NUM_DAYS {
            println!("After {} day(s) there are {} fish", day, total_pop);
        }
    }
}
