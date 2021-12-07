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

    let steps_per_position: Vec<Vec<u32>> = (0..=max_position)
        .map(|target_position| {
            crabs
                .iter()
                .map(|&pos| (pos as i32 - target_position as i32).abs() as u32)
                .collect()
        })
        .collect();

    let min_fuel_linear: u32 = steps_per_position
        .iter()
        .map(|steps| steps.iter().sum())
        .min()
        .unwrap();

    println!("{}", min_fuel_linear);

    let min_fuel_increasing: u32 = steps_per_position
        .iter()
        .map(|steps| steps.iter().map(|&pos| pos * (pos + 1) / 2).sum())
        .min()
        .unwrap();

    println!("{}", min_fuel_increasing);
}
