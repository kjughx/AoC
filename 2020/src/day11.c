#include "libpj.h"
#include <math.h>


#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

#define IS_EMPTY(G, x, y) ((*ma_at((G), (x), (y)) == 'L' ))
#define IS_OCCUPIED(G, x, y) (ma_inbounds((G), (x), (y)) && (*ma_at((G), (x), (y)) == '#'))
#define IS_FLOOR(G, x, y) (ma_inbounds((G), (x), (y)) && (*ma_at((G), (x), (y)) == '.'))

typedef struct {
  char *items;
  size_t nx;
  size_t ny;
} Grid;

#define NEIGHBORS 8
Vector2 neighbors[NEIGHBORS] = {{0, 1}, {1, 1}, {1, 0}, {-1, 1}, {-1, 0}, {-1, -1}, {0, -1}, {1, -1}};

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  ssize_t ny = lines.count;
  ssize_t nx = sb.count / lines.count;
  printf("nx=%zu ny=%zu\n", nx, ny);

  Grid Gold = {.nx = nx, .ny = ny};
  Grid Gnew = {.nx = nx, .ny = ny};
  ma_init(&Gold);
  ma_init(&Gnew);

  for (size_t y = 0; y < ny; ++y) {
    String_Builder line = sv_to_sb(lines.items[y]);
    for (size_t x = 0; x < nx; ++x) {
      *ma_at(&Gold, x, y) = line.items[x];
      *ma_at(&Gnew, x, y) = line.items[x];
    }
  }
  char *tmp;
  for (size_t i = 0;; ++i) {
    bool changed = false;

    tmp = Gold.items;
    Gold.items = Gnew.items;
    Gnew.items = tmp;

    for (ssize_t y = 0; y < ny; ++y) {
      for (ssize_t x = 0; x < nx; ++x) {
        int empties = 0;
        for (size_t n = 0; n < NEIGHBORS; ++n) {
          int dx = neighbors[n].x;
          int dy = neighbors[n].y;

#ifdef PART1
          empties += !IS_OCCUPIED(&Gold, x + dx, y + dy);
#else
          ssize_t i = 1;
          while (IS_FLOOR(&Gold, x + i * dx, y + i * dy)) i++;
          empties += !IS_OCCUPIED(&Gold, x + i * dx, y + i * dy);
#endif
        }

        *ma_at(&Gnew, x, y) = *ma_at(&Gold, x, y);

        if (IS_EMPTY(&Gold, x, y)) {
          if (empties == NEIGHBORS) {
            changed = true;
            *ma_at(&Gnew, x, y) = '#';
          }
        } else if (IS_OCCUPIED(&Gold, x, y)){
#ifdef PART1
          if (empties <= 4) {
#else
          if (empties <= 3) {
#endif
            changed = true;
            *ma_at(&Gnew, x, y) = 'L';
          }
        }
      }
    }

    if (!changed) {
      break;
    }
  }

  for (ssize_t y = 0; y < ny; ++y) {
    for (ssize_t x = 0; x < nx; ++x) {
      printf("%c", *ma_at(&Gnew, x, y));
    }
    printf("\n");
  }

  int ans = 0;
  for (ssize_t x = 0; x < nx; ++x) {
    for (ssize_t y = 0; y < ny; ++y) {
      ans += (*ma_at(&Gnew, x, y) == '#');
    }
  }
  printf("%d\n", ans);

}
