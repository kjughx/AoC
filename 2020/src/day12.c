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

#ifdef PART1
  {
    Vector2 v  = {0};
    Vector2 dv = {.x = 1};

    sb_foreach_line(&sb, line) {
      char c;
      int d;
      sscanf(line, "%c%d", &c, &d);
      if (c == 'N') v.y -= d;
      if (c == 'S') v.y += d;
      if (c == 'E') v.x += d;
      if (c == 'W') v.x -= d;
      if (c == 'L') {
        d = d / 90;
        while (d--) {
          swap(dv.x, dv.y);
          dv.y *= -1;
        }
      }
      if (c == 'R') {
        d = d / 90;
        while (d--) {
          swap(dv.x, dv.y);
          dv.x *= -1;
        }
      }
      if (c == 'F') {
        v.x += d * dv.x;
        v.y += d * dv.y;
      }
    }
    printf("%zd\n", abs(v.x) + abs(v.y));
  }
#endif

#ifdef PART2
  {
    Vector2 v  = {0};
    Vector2 w = {.x = 10, .y = -1};
    sb_foreach_line(&sb, line) {
      char c;
      int d;
      sscanf(line, "%c%d", &c, &d);
      if (c == 'N') w.y -= d;
      if (c == 'S') w.y += d;
      if (c == 'E') w.x += d;
      if (c == 'W') w.x -= d;
      if (c == 'L') {
        d = d / 90;
        while (d--) {
          swap(w.x, w.y);
          w.y *= -1;
        }
      }
      if (c == 'R') {
        d = d / 90;
        while (d--) {
          swap(w.x, w.y);
          w.x *= -1;
        }
      }
      if (c == 'F') {
        v.x += d * w.x;
        v.y += d * w.y;
      }
      
      printf("%zd %zd\n", v.x, v.y);
    }
    printf("%zd\n", abs(v.x) + abs(v.y));
  }
#endif
}
