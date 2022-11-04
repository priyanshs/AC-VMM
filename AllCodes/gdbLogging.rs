use std::process::Command;
use std::process::Stdio;
use std::vec::Vec;
use std::fs::OpenOptions;
use std::io::{Write, Read, Error};
use std::env;
use std::fs::File;
use std::time::Instant;
use std::io::{self, prelude::*, BufReader};
pub fn instances(st:String)->Vec<String>{
    let mut s=st.clone();
    let mut ret = Vec::new();
    while true{
        let mut temp=s.clone();
        let cond=s.find("1: {");
        if cond.is_none(){
            break;
        }
        let brack1=cond.unwrap();
        s=s[brack1..].to_string();
        let brack2=s.find("}").unwrap();
        s=s[brack2..].to_string();
        let brack3=s.find("= {").unwrap();
        s=s[brack3..].to_string();
        let brack4=s.find("}").unwrap();
        s=s[brack4..].to_string();
        ret.push(temp[brack1+3..brack1+brack2+brack3+brack4+1].to_string());
    }
    return ret;
}
pub fn gdbLog(st:String){
    let mut compile = Command::new("sh");
    let mut comp="g++ -g ".to_owned()+&st+".cpp";
    compile.arg("-c").arg(comp);
    let x=compile.output().expect("failed to execute process");
    let mut gdb=Command::new("sh");
    gdb.arg("-c").arg("bash gdb.sh");
    let x=gdb.output().expect("failed to execute process").stdout;
    let s = String::from_utf8(x).expect("Found invalid UTF-8");
    let vec=instances(s);
    let mut file = File::create(st.clone()+".txt");
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open(st.clone()+".txt")
        .unwrap();
    for e in vec.iter(){
        let x=e.clone();
        file.write_all(x.as_bytes());
        file.write_all(b"\n");
    }
}
pub fn timeCheck(st:String){
    let mut comp="g++ -g ".to_owned()+&st+".cpp";
    let mut compile = Command::new("sh");
    compile.arg("-c").arg(comp);
    let x=compile.output().expect("failed to execute process").stdout;
    let now = Instant::now();
    let mut compile = Command::new("sh");
    compile.arg("-c").arg("./a.out");
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
        gdbLog(line.as_ref().unwrap().clone());
        timeCheck(line.as_ref().unwrap().clone());
    }
}
