fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        std::process::exit(1);
    }

    let crab_file = std::fs::read_to_string(&args[1]).expect("Cannot open file");

    let crabs: Vec<u32> = crab_file
        .trim()
        .split(",")
        .map(|n| n.parse().unwrap())
        .collect();
    let max_position = *crabs.iter().max().unwrap();

    let min_fuel_linear = (0..=max_position)
        .map(|target_position| {
            crabs
                .iter()
                .map(|&pos| (pos as i32 - target_position as i32).abs() as u32)
                .sum::<u32>()
        })
        .min()
        .unwrap();

    println!("{:?}", min_fuel_linear);
}
