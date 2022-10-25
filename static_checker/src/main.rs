use ignore::Walk;
// use rayon::prelude::*;
use std::path::{Path, PathBuf};
use structopt::StructOpt;
use serde_json;
use std::io::Write;

mod lib;
mod preprocessors;

#[derive(StructOpt, Debug)]
#[structopt(set_term_width = 80)]
struct Cli {
    #[structopt(default_value="./src/test/orig.rs")]
    source: PathBuf,
    /// Source file to check for plagiarism.
    // source: PathBuf,
    /// Targets to compare against the source file.
    /// If a target is a directory, it is searched recursively.
    #[structopt(default_value = "./")]
    targets: Vec<PathBuf>,
}

fn main() {
    let cli = Cli::from_args();
    let targets = &walk_directories(&cli.targets);
    // write to this file as well as DB
    let output_file = "results.json";
    // dbg!(&cli.source);
    // dbg!(targets);

    // create a new Box for the CPreprocessor and use that wih Rust code
    let preprocessor = Some(Box::new(lib::preprocessors::CPreprocessor::new()));

    for result in lib::detect(&cli.source, &targets, preprocessor.as_deref()) {
        match result {
            // set similarity threshold to 1% for convenience
            // should output all files in most cases
            Ok((target, score)) if score >= 1. / 100. => {
                // DB handling goes here
                // temporarily write to a JSON file
                let data = serde_json::json!({
                    "file": target,
                    "similarity": score * 100.
                });
                // debug output to check if preprocessor works
                // println!("\"{}\" : {:.2}%", target.display(), score * 100.);
                // append to file rather than replace contents
                let mut file_ref = std::fs::OpenOptions::new().append(true).open(output_file).unwrap();

                file_ref.write_all(serde_json::to_string_pretty(&data).unwrap().as_bytes()).expect("appending data failed");

                // writes replacing all content, so only last entry is present at the end
                // std::fs::write(
                //     output_file,
                //     serde_json::to_string_pretty(&data).unwrap()
                // );
            }
            Err(e) => {
                eprintln!("{}", e);
            }
            _ => {},
        }
    }
}

fn walk_directories<P: AsRef<Path>>(paths: &[P]) -> Vec<PathBuf> {
    paths
        .iter()
        .flat_map(|path| {
            Walk::new(path)
                .inspect(|entry| {
                    if let Err(e) = entry {
                        eprintln!("{}", e);
                    }
                })
                .filter_map(Result::ok)
                // Filter: only files; ignore directories
                .filter(|entry| entry.file_type().map_or(false, |e| e.is_file()))
                .map(|entry| entry.into_path())
        })
        .collect()
}
