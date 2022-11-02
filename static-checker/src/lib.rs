use rayon::prelude::*;
use std::fs;
use std::path::{Path, PathBuf};

pub mod preprocessors;

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("\"{0}\": IO error: {1}")]
    IoError(PathBuf, std::io::Error),
}
pub type Result<T> = std::result::Result<T, Error>;

/// Compare `source` to all `targets` and return `targets` with their similarity score
pub fn detect<
    P1: AsRef<Path> + Eq + Sync,
    P2: AsRef<Path> + Eq,
    PP: preprocessors::Preprocessor + ?Sized + Sync,
>(
    source: P1,
    targets: &[P2],
    preprocessor: Option<&PP>,
) -> Vec<Result<(PathBuf, f64)>> {
    let source_content = match parse_content(&source, preprocessor) {
        Ok(content) => content,
        Err(e) => {
            return vec![Err(e)];
        }
    };

    let targets: Vec<&Path> = targets.iter().map(AsRef::as_ref).collect();
    targets
        .into_par_iter()
        .filter(|target| target.canonicalize().unwrap() != source.as_ref().canonicalize().unwrap())
        .map(|target| parse_content(target, preprocessor).map(|content| (target, content)))
        .map(|result| {
            result.map(|(target, target_content)| {
                (
                    target.to_owned(),
                    similarity(&source_content, &target_content),
                )
            })
        })
        .collect()
}

/// Calculates strings similarity score
fn similarity(a: &str, b: &str) -> f64 {
    strsim::normalized_levenshtein(a, b)
}

/// Returns the contents of a file and runs a preprocessor
fn parse_content<P: AsRef<Path>, PP: preprocessors::Preprocessor + ?Sized>(
    path: P,
    preprocessor: Option<&PP>,
) -> Result<String> {
    match fs::read_to_string(&path) {
        Ok(content) => match preprocessor {
            Some(pp) => Ok(pp.process(&content)),
            None => Ok(content),
        },
        Err(e) => Err(Error::IoError(path.as_ref().to_owned(), e)),
    }
}
