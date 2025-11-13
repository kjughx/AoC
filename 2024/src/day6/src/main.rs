use std::collections::HashSet;

fn walk(mut r: isize, mut c: isize, grid: Vec<Vec<char>>) -> bool {
    let (mut dr, mut dc) = (-1, 0);
    let (R, C) = (grid.len(), grid[0].len());
    let mut vis: HashSet<(isize, isize, isize, isize)> = HashSet::new();
    vis.insert((r, c, dr, dc));

    loop {
        let (nr, nc) = ((r as isize + dr), (c as isize + dc));
        if nr < 0 || nc < 0 || nr >= R as isize || nc >= C as isize {
            break;
        }
        let key = (nr, nc, dr, dc);
        if vis.contains(&key)  {
            return false;
        }

        if grid[nr as usize][nc as usize] != '#' {
            (r, c) = (nr, nc);
            vis.insert(key);
        } else{
            (dr, dc) = (dc, -dr);
        }
    }
    
    return true;
}

fn main() {
    let input = std::fs::read_to_string("../../inputs/day6").unwrap();

    let grid: Vec<Vec<char>> = input
        .trim()
        .lines()
        .map(|line| line.chars().collect())
        .collect();

    let (mut r, mut c) = (0, 0);
    'll: for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == '^' {
                (r, c) = (i, j);
                break 'll;
            }
    }}

    let mut loops = 0;

    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            let mut ngrid = grid.clone();
            ngrid[i][j] = '#';
            if !walk(r as isize, c as isize, ngrid) {
                loops += 1;
            }

        }
    }
    println!("{loops}");

}
