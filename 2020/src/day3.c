#include "libpj.h"

typedef struct {
  char *items;
  size_t nx;
  size_t ny;
} Grid;

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;
  Grid G = {.nx = 31, .ny = 323};
  ma_init(&G);

  int r = 0;
  sb_foreach_line(&sb, line) {
    for(size_t x = 0; x < strlen(line); ++x) {
      *ma_at(&G, x, r) = line[x];
    }
    r++;
  }

  #define SLOPES 5
  Vector2 ps[SLOPES] = {0};
  Vector2 slopes[SLOPES] = {{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2}};
  int ans[SLOPES] = {0};
  while (1) {
    int done = 0;
    for (size_t i = 0; i < SLOPES; ++i) {
      ps[i].x = (ps[i].x + slopes[i].x) % G.nx;
      ps[i].y = (ps[i].y + slopes[i].y);
      if (ps[i].y >= G.ny) {
        done++;
      } else {
        if (*ma_at(&G, ps[i].x, ps[i].y) == '#') {
          ans[i]++;
        }
      }
    }
    if (done == SLOPES) break;
  }
  size_t a = 1;
  for (size_t i = 0; i < SLOPES; ++i) {
    a *= ans[i];
  }
  printf("%zu\n", a);
}
