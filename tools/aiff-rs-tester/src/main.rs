use aiff::reader::AiffReader;
use std::fs::File;

fn main() {
    let mut args_iter = std::env::args();
    let _cmd = args_iter.next();
    let filename = args_iter.next().expect("No filename");

    let file = File::open(filename).expect("Can't open file");
    let mut reader = AiffReader::new(file);
    match reader.read() {
        Ok(()) => {},
        Err(e) => {
            eprintln!("* ERROR: Can't read file: {:?}", e);
            std::process::exit(-1);
        }
    }
    let form = match reader.form().as_ref() {
        Some(f) => f,
        None => {
            eprintln!("* ERROR: Can't find the FORM chunk");
            std::process::exit(-1);
        }
    };
    let comm = match form.common().as_ref() {
        Some(c) => c,
        None => {
            eprintln!("* ERROR: Can't find the COMM chunk");
            std::process::exit(-1);
        }
    };

    // convert sample data to f64

    let mut samples : Vec<f64> = vec![];
    let mut compr_type = "pcm_bei";
    //let comm_compr_type = &comm.compression_type;
    let comm_compr_type: Option<String> = None;
    match comm_compr_type {
        None => {
            if comm.bit_rate <= 8 {
                for d in reader.samples::<i8>() {
                    samples.push(d as f64);
                }
            } else if comm.bit_rate <= 16 {
                for d in reader.samples::<i16>() {
                    samples.push(d as f64);
                }
            } else if comm.bit_rate <= 24 {
                for d in reader.samples::<i32>() {
                    samples.push(d as f64);
                }
            } else if comm.bit_rate <= 32 {
                for d in reader.samples::<i32>() {
                    samples.push(d as f64);
                }
            } else {
                eprintln!("* ERROR: INVALID BITRATE: {}", comm.bit_rate);
                std::process::exit(-1);
            }
        },
        Some(ct) => {
            if ct == "fl32" {
                compr_type = "pcm_bef";
                /* enable for f32
                for d in reader.samples::<f32>() {
                    samples.push(d as f64);
                }
                */
            } else if ct == "fl64" {
                compr_type = "pcm_bef";
                // TODO: enable if f64 gets implemented
                for d in vec![] { // reader.samples::<f64>() {
                    samples.push(d);
                }
            } else {
                eprintln!("* ERROR: unsupported compression type: {}", ct);
                std::process::exit(-1);
            }
        }
    }

    // print json

    println!("{{");
    println!("    \"format\": \"-unsupported-\",");
    if comm.sample_rate.is_finite() {
        println!("    \"sampleRate\": {},", comm.sample_rate);
    } else {
        println!("    \"sampleRate\": \"{}\",", comm.sample_rate);
    }
    println!("    \"channels\": {},", comm.num_channels);
    println!("    \"codec\": \"{}\",", compr_type);
    println!("    \"sampleSize\": {},", comm.bit_rate);

    // TODO: implement printing values for these
    println!("    \"markers\": \"-unsupported-\",");
    println!("    \"comments\": \"-unsupported-\",");
    println!("    \"inst\": \"-unsupported-\",");
    println!("    \"midi\": \"-unsupported-\",");
    println!("    \"aesd\": \"-unsupported-\",");
    println!("    \"appl\": \"-unsupported-\",");
    println!("    \"name\": \"-unsupported-\",");
    println!("    \"auth\": \"-unsupported-\",");
    println!("    \"(c)\": \"-unsupported-\",");
    println!("    \"anno\": \"-unsupported-\",");
    println!("    \"id3\": \"-unsupported-\",");
    println!("    \"chan\": \"-unsupported-\",");
    println!("    \"hash\": \"-unsupported-\",");

    // print sample data
    println!("    \"samplesPerChannel\": {},", comm.num_sample_frames);
    println!("    \"startSamples\": [");
    let start_einx = samples.len().min(300*comm.num_channels as usize);
    print_sample_data(comm.num_channels as usize, &samples[0..start_einx]);
    println!("    ],");

    println!("    \"endSamples\": [");
    let mut end_sinx = 0;
    if samples.len() > 30*comm.num_channels as usize {
        end_sinx = samples.len() - 30*comm.num_channels as usize;
    }
    print_sample_data(comm.num_channels as usize, &samples[end_sinx..]);
    println!("    ]");

    println!("}}");
}

fn print_sample_data(num_channels: usize, samples: &[f64]) {
    let samples_per_channel = samples.len() / num_channels;
    for ch in 0..num_channels {
        print!("        [ ");
        let mut pos = 0;
        while pos < samples_per_channel {
            if pos != 0 {
                print!(", ");
            }
            let s = samples[pos * num_channels + ch];
            if s.is_finite() {
                print!("{:.6}", s);
            } else {
                let str = format!("\"{:.6}\"", s);
                print!("{}", str.to_lowercase());
            }
            pos += 1;
        }
        if ch < num_channels-1 {
            println!(" ],");
        } else {
            println!(" ]");
        }
    }
}