use ignore::Walk;
use rayon::prelude::*;
use std::path::{Path, PathBuf};
use structopt::StructOpt;
// use std::process::Command;

mod lib;
mod preprocessors;

#[derive(StructOpt, Debug)]
#[structopt(set_term_width = 80)]
struct Cli {
    /// Only show files with specified similarity percentage.
    #[structopt(short, long, default_value = "80")]
    similarity: f64,

    /// File preprocessor to use.
    ///
    /// * "asm": x86 GAS assembly
    /// * "c": C programming language
    /// * "text": Basic text preprocessing
    /// * "none": Disable preprocessing {n}
    #[structopt(
        short,
        long,
        default_value = "asm",
        possible_values = &["asm", "c", "text", "none"],
        verbatim_doc_comment,
    )]
    preprocessor: String,

    /// Source file to check for plagiarism.
    source: PathBuf,
    /// Targets to compare against the source file.
    /// If a target is a directory, it is searched recursively.
    #[structopt(default_value = "./")]
    targets: Vec<PathBuf>,
}

fn main() {
    let cli = Cli::from_args();
    let targets = walk_directories(&cli.targets);
    dbg!(targets);
    // TODO: solve preprocessor issue as its needed in both lib and main
    let preprocessor = get_preprocessor(&cli.preprocessor);

    // TODO: uncomment later to detect all files and store similarity score
    // for result in lib::detect(&cli.source, &targets, preprocessor.as_deref()) {
    //     match result {
    //         Ok((target, score)) if score >= cli.similarity / 100. => {
    //             println!("\"{}\" : {:.2}%", target.display(), score * 100.);
    //         }
    //         Err(e) => {
    //             eprintln!("{}", e);
    //         }
    //         _ => {}
    //     }
    // }
}

fn get_preprocessor(pp: &str) -> Option<Box<dyn preprocessors::Preprocessor + Sync>> {
    match pp {
        "asm" => Some(Box::new(preprocessors::AsmPreprocessor::new())),
        "c" => Some(Box::new(preprocessors::CPreprocessor::new())),
        "text" => Some(Box::new(preprocessors::TextPreprocessor::new())),
        "none" => None,
        _ => unreachable!(),
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
