fn error_score(c: char) -> u32 {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        _ => 25137
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        std::process::exit(1);
    }

    let mut total_error_score = 0;
    std::fs::read_to_string(&args[1])
        .expect("Cannot open file")
        .lines()
        .for_each(|line| {
            let mut stack: Vec<char> = vec![];
            for c in line.chars() {
                if c == '(' || c == '[' || c == '{' || c == '<' {
                    stack.append(&mut vec![c]);
                } else {
                    let ok = match stack.pop().unwrap() {
                        '(' => c == ')',
                        '[' => c == ']',
                        '{' => c == '}',
                        _ => c == '>',
                    };

                    if !ok {
                        total_error_score += error_score(c);
                    }
                }
            }
        });

        println!("{}", total_error_score);
}
