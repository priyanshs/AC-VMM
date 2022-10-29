use std::process::Command;
use std::process::Stdio;
use std::vec::Vec;
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
fn main() {
    let mut compile = Command::new("sh");
    compile.arg("-c").arg("g++ -g hello.cpp");
    let x=compile.output().expect("failed to execute process").stdout;
    let mut gdb=Command::new("sh");
    gdb.arg("-c").arg("bash run.sh");
    let x=gdb.output().expect("failed to execute process").stdout;
    let s = String::from_utf8(x).expect("Found invalid UTF-8");
    let vec=instances(s);
    println!("{:?}",vec);
}
