use std::process::Command;
use std::process::Stdio;
use std::vec::Vec;
use std::fs::OpenOptions;
use std::io::{Write, Read, Error};
use std::env;
use std::fs::File;
use std::time::Instant;
use std::io::{self, prelude::*, BufReader};
pub fn timeCheckPy(st:String){
    let now = Instant::now();
    let mut compile = Command::new("sh");
    let mut comp="python ".to_owned()+&st+".py";
    compile.arg("-c").arg(comp);
    let x=compile.output().expect("failed to execute process").stdout;
    let elapsed = now.elapsed().as_nanos();
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open("time")
        .unwrap();
    let x=elapsed.to_string();
    writeln!(file, "{}",st.clone()+","+&x);
}
fn main() {
    let mut file = File::create("time");
    let file = File::open("submissions").unwrap();
    let reader = BufReader::new(file);
    for line in reader.lines() {
        timeCheckPy(line.as_ref().unwrap().clone());
    }
}