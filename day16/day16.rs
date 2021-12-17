struct Packet {
    version: u8,
    version_sum: u32,
    typeid: u8,
    subpackets: Vec<Packet>,
    value: u64,
}

impl Packet {
    pub fn from_bitstream(bits: &mut String) -> Self {
        let version = u8::from_str_radix(bits.drain(..3).as_str(), 2).unwrap();
        let typeid = u8::from_str_radix(bits.drain(..3).as_str(), 2).unwrap();

        let mut subpackets = Vec::new();
        let value: u64 = if typeid == 4 {
            let mut literal = String::new();
            loop {
                let cont = bits.drain(..1).next().unwrap();
                literal.push_str(bits.drain(..4).as_str());
                if cont == '0' {
                    break;
                }
            }

            u64::from_str_radix(&literal, 2).unwrap()
        } else {
            let length_type = bits.drain(..1).next().unwrap();
            if length_type == '0' {
                let num_bits = usize::from_str_radix(bits.drain(..15).as_str(), 2).unwrap();
                let mut remaining: String = bits.drain(..num_bits).collect();
                while !remaining.is_empty() {
                    let subpacket = Packet::from_bitstream(&mut remaining);
                    subpackets.push(subpacket);
                }
            } else {
                let num_packets = usize::from_str_radix(bits.drain(..11).as_str(), 2).unwrap();
                for _ in 0..num_packets {
                    let subpacket = Packet::from_bitstream(bits);
                    subpackets.push(subpacket);
                }
            }

            let subpacket_values = subpackets.iter().map(|p| p.value);
            match typeid {
                0 => subpacket_values.sum::<u64>(),
                1 => subpacket_values.product::<u64>(),
                2 => subpacket_values.min().unwrap(),
                3 => subpacket_values.max().unwrap(),
                _ => {
                    let first = subpackets[0].value;
                    let second = subpackets[1].value;
                    match typeid {
                        5 => (first > second) as u64,
                        6 => (first < second) as u64,
                        _ => (first == second) as u64,
                    }
                }
            }
        };

        let version_sum: u32 =
            version as u32 + subpackets.iter().map(|p| p.version_sum as u32).sum::<u32>();

        Self {
            version,
            version_sum,
            typeid,
            subpackets,
            value,
        }
    }

    pub fn from_hexstream(hexstream: &str) -> Self {
        let mut bitstream = String::new();
        hexstream
            .chars()
            .map(|h| format!("{:04b}", u8::from_str_radix(&h.to_string(), 16).unwrap()))
            .for_each(|bin| bitstream.push_str(&bin));

        Self::from_bitstream(&mut bitstream)
    }

    #[allow(dead_code)]
    fn pprint_level(&self, level: usize) {
        println!(
            "{}Version={}, type={}, value={}",
            if level > 0 {
                " ".repeat(level * 4)
            } else {
                "".to_string()
            },
            self.version,
            self.typeid,
            self.value
        );
        for packet in &self.subpackets {
            packet.pprint_level(level + 1);
        }
    }

    #[allow(dead_code)]
    pub fn pprint(&self) {
        self.pprint_level(0);
    }
}

impl std::fmt::Debug for Packet {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(
            f,
            "Packet(version={}, typeid={}, value={:?} subpackets={:?})",
            self.version, self.typeid, self.value, self.subpackets
        )
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let packet = Packet::from_hexstream(std::fs::read_to_string(&args[1]).unwrap().trim());

    println!("Sum of packet versions: {}", packet.version_sum);
    println!("Packet value: {}", packet.value);
}
