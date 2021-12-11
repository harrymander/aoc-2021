fn error_score(c: char) -> u32 {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        _ => 25137,
    }
}

fn completion_score(c: char) -> u32 {
    match c {
        ')' => 1,
        ']' => 2,
        '}' => 3,
        _ => 4,
    }
}

fn match_char(c: char) -> char {
    match c {
        '(' => ')',
        '[' => ']',
        '{' => '}',
        _ => '>',
    }
}

const COMPLETE_MULTIPLIER: u64 = 5;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        std::process::exit(1);
    }

    let mut total_error_score = 0;
    let mut completion_scores: Vec<u64> = vec![];
    std::fs::read_to_string(&args[1])
        .expect("Cannot open file")
        .lines()
        .for_each(|line| {
            let mut stack: Vec<char> = vec![];
            let mut valid = true;
            for c in line.chars() {
                if c == '(' || c == '[' || c == '{' || c == '<' {
                    stack.append(&mut vec![c]);
                } else {
                    let popped = stack.pop();
                    if popped.is_some() && match_char(popped.unwrap()) != c {
                        total_error_score += error_score(c);
                        valid = false;
                    }
                }
            }

            if valid && !stack.is_empty() {
                let mut score: u64 = 0;
                while !stack.is_empty() {
                    let c = stack.pop().unwrap();
                    score *= COMPLETE_MULTIPLIER;
                    score += completion_score(match_char(c)) as u64;
                }
                completion_scores.append(&mut vec![score]);
            }
        });

    completion_scores.sort_unstable();
    let median_completion_score = completion_scores[completion_scores.len() / 2];

    println!("{}", total_error_score);
    println!("{}", median_completion_score);
}
