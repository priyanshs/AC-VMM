use ignore::Walk;
// use rayon::prelude::*;
use std::path::{Path, PathBuf};
use structopt::StructOpt;
use serde_json;
use std::io::Write;
use std::collections::HashMap;

mod lib;
mod preprocessors;

#[derive(StructOpt, Debug)]
#[structopt(set_term_width = 80)]
struct Cli {
    // #[structopt(default_value="./src/test/orig.rs")]
    // source: PathBuf,
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
    //write to this file as well as DB
    let output_file = "results.json";
    //map to reduce redundant computation
    //we want to avoid comaparisons like (1,2) and (2,1)
    //as they are commutative
    let mut added_set:HashMap<String, bool> = HashMap::new();
    //clear "results.json" before appending to it
    let _f = std::fs::write(output_file, "");
    // dbg!(&cli.source);
    // dbg!(targets);

    //create a new Box for the CPreprocessor and use that wih Rust code
    let preprocessor = Some(Box::new(lib::preprocessors::CPreprocessor::new()));

    //data array to write to JSON file
    let mut data = serde_json::json!({"data": []});

    //initialize map with false
    for file in targets.iter() {
        added_set.insert(file.display().to_string(), false);
    }

    //iterate over all submissions
    for source in targets.iter(){
        let mut source_data = serde_json::json!({
            "source_name": source,
            "checker_result": [],
        });
        for result in lib::detect(source, &targets, preprocessor.as_deref()) {
            match result {
                    // set similarity threshold to 1% for convenience
                    // should output all files in most cases
                    Ok((target, score)) if score >= 0. => {
                        // DB handling goes here
                        // temporarily write to a JSON file
                        if (source != &target) && !(*(added_set.get(&target.display().to_string()).unwrap())) {
                            // write data to file only for distinct source and target
                            // debug output to check if preprocessor works
                            // println!("\"{}\" : {:.2}%", target.display(), score * 100.);
                            // append to file rather than replace contents
                            source_data["checker_result"].as_array_mut().unwrap().push(serde_json::json!({
                                "target_name": target,
                                "similarity_score": score,
                            }));
                        }

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
        //this file is compared with all other files
        added_set.insert(source.display().to_string(), true);
        data["data"].as_array_mut().unwrap().push(source_data);
    }

    // write final array to files
    let mut file_ref = std::fs::OpenOptions::new().append(true).open(output_file).unwrap();
    file_ref.write_all(serde_json::to_string_pretty(&data).unwrap().as_bytes()).expect("appending data failed");
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
