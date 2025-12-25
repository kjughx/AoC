#include "libpj.h"

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  char *p = sb.items;
  size_t areas[6];
  for (size_t i = 0; i < 6; ++i) {
    size_t area = 0;
    while (strncmp(p, "\n\n", 2) != 0) {
      if (*p++ == '#') area++;
    }
    areas[i] = area;
    p += 2;
  }
  sb.count -= (p - sb.items);
  sb.items = p;

  size_t n = 0;
  sb_foreach_line(&sb, line) {
    int w,h;
    int xs[6];
    sscanf(line, "%dx%d: %d %d %d %d %d %d", &w, &h, &xs[0],&xs[1],&xs[2],&xs[3],&xs[4],&xs[5]);
    int total_area = 0;
    for (size_t i = 0; i < 6; ++i) {
      total_area += xs[i] * areas[i];
    }
    if (total_area <= w * h) n++;
  }
  printf("%zu\n", n);
}
