use std::time::Instant;

fn bench<F, R>(f: F) -> R
where
    F: FnOnce() -> R,
{
    let t0 = Instant::now();
    let result = f(); // Call the function and store the result
    println!("time used: {:?}", Instant::now().duration_since(t0));
    result // Return the result of the function
}
#[inline(always)]
fn run(mut a: usize) -> (usize, usize) {
    let o;
    unsafe {
        std::arch::asm!(r#"
        push %rcx
        push %rdx
        call _run
        pop %rdx
        pop %rcx
    "#, inout("r8") a, out("rax") o, options(att_syntax))
    };

    return (a, o);
}

fn runall(mut a: usize) -> [usize; 64] {
    let mut v = [0; 64];
    let mut i = 0;
    loop {
        (a, v[i]) = run(a);
        i += 1;

        if a == 0 {
            break;
        }
    }

    return v;
}

#[inline(always)]
fn f(aa: usize, prog: &[usize], i: usize) -> Option<usize> {
    if i == 0 {
        for a in 0..8 {
            if run((aa << 3) | a).1 == prog[0] {
                return Some((aa << 3) | a);
            }
        }

        return None;
    }

    for a in 0..8 {
        if run((aa << 3) | a).1 == prog[i] {
            let aaa = f((aa << 3) | a, prog, i - 1);
            if aaa.is_some() {
                return aaa;
            }
        }
    }

    return None;
}

fn part1() -> [usize; 64] {
    let input = include_str!("../program")
        .split('\n')
        .collect::<Vec<&str>>();
    let a: usize = unsafe {
        str::parse::<usize>(input[0].split(" ").collect::<Vec<&str>>()[2]).unwrap_unchecked()
    };
    runall(a)
}

fn part2() -> usize {
    let input = include_str!("../program")
        .split('\n')
        .collect::<Vec<&str>>();
    let prog: Vec<usize> = unsafe {
        input[4]
            .split_once(": ")
            .unwrap_unchecked()
            .1
            .split(',')
            .map(|c| str::parse::<usize>(c).unwrap_unchecked())
            .collect()
    };
    let a = f(0, &prog, prog.len() - 1).unwrap();
    return a;
}

fn main() {
    println!("{:?}", bench(part1));
    println!("{}", bench(part2));
}
