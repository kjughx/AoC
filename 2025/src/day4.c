#include "libpj.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

int main(void) {
  Grid G = grid_read(stdin);

#ifdef PART1
  u64 part1 = 0;
  for (size_t y = 0; y < G.ny; ++y) {
    for (size_t x = 0; x < G.nx; ++x) {
      if (*ma_at(&G, x, y) != '@')
        continue;
      int n = 0;
      for (ssize_t dx = -1; dx <= 1; ++dx) {
        for (ssize_t dy = -1; dy <= 1; ++dy) {
          ssize_t nx = (ssize_t)x + dx;
          ssize_t ny = (ssize_t)y + dy;
          if (!ma_inbounds(&G, nx, ny)) {
            n++;
            continue;
          }
          n += (*ma_at(&G, nx, ny) == '.');
        }
      }
      if (n > 4)
        part1++;
    }
  }
  printf("%ld\n", part1);
#endif
#ifdef PART2
  Grid Gnew = {.nx = G.nx, .ny = G.ny};
  ma_init(&Gnew);

  bool removed = false;
  u64 part2 = 0;
  do {
    ma_fill(&Gnew, '.');
    removed = false;
    for (size_t y = 0; y < G.ny; ++y) {
      for (size_t x = 0; x < G.nx; ++x) {
        if (*ma_at(&G, x, y) != '@')
          continue;
        int n = 0;
        for (ssize_t dx = -1; dx <= 1; ++dx) {
          for (ssize_t dy = -1; dy <= 1; ++dy) {
            ssize_t nx = (ssize_t)x + dx;
            ssize_t ny = (ssize_t)y + dy;
            if (!ma_inbounds(&G, nx, ny)) {
              n++;
              continue;
            }
            n += (*ma_at(&G, nx, ny) == '.');
          }
        }
        if (n > 4) {
          removed = true;
          part2++;
        } else
          *ma_at(&Gnew, x, y) = *ma_at(&G, x, y);
      }
    }
    swap(Gnew.items, G.items);
  } while (removed);

  printf("%ld\n", part2);
#endif
}
