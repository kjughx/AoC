#include "libpj.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  i32 dial = 50;
  int ans = 0;
  sb_foreach_line(&sb, line) {
    char dir;
    int d;
    expect(sscanf(line, "%c%d", &dir, &d) == 2);
    if (dir == 'R') {
#ifdef PART2
      while (d > 100) {
        ans++;
        d -= 100;
      }
      if (dial + d > 100)
        ans++;
#endif
      dial = (dial + d) % 100;
    }
    if (dir == 'L') {
#ifdef PART2
      int p = dial;
      while (d > 100) {
        ans++;
        d -= 100;
      }
#endif
      dial = (dial - d) % 100;
      if (dial < 0) {
#ifdef PART2
        if (p)
          ans++;
#endif
        dial = 100 + dial;
      }
    }
    if (dial == 0)
      ans++;
  }
  printf("%d\n", ans);
}
