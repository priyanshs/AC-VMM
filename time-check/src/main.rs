use std::process::Command;
use std::time::Instant;
use std::env;
use std::fs::OpenOptions;
use std::io::Write;
fn main() {
    let args: Vec<String> = env::args().collect();
    let mut comp="g++ -g ".to_owned()+&args[1];
    let mut compile = Command::new("sh");
    compile.arg("-c").arg(comp);
    let x=compile.output().expect("failed to execute process").stdout;
    let now = Instant::now();
    let mut compile = Command::new("sh");
    compile.arg("-c").arg("./a.out");
    let x=compile.output().expect("failed to execute process").stdout;
    let elapsed = now.elapsed().as_nanos();
    let mut file = OpenOptions::create_new()
        .write(true)
        .append(true)
        .open("allFiles.txt")
        .unwrap();
    let x=elapsed.to_string();
    writeln!(file, "{}",args[1].clone()+","+&x);
}