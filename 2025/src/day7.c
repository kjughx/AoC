#include "libpj.h"

typedef struct {
  Vector2 *items;
  size_t count;
  size_t capacity;
} Beam;

int main(void) {
  Grid G = grid_read(stdin);
  Vector22Int beam = {0};
  Vector22Int new = {0};

  size_t sx = 0, sy = 0;
  u64 part1 = 0;
  for (size_t x = 0; x < G.nx; ++x) {
    for (size_t y = 0; y < G.ny; ++y) {
      if (*ma_at(&G, x, y) == 'S') {
        sx = x;
        sy = y;
        goto l1;
      }
    }
  }
l1:

  ht_insert(&beam, ((Vector2){.x = sx, .y = sy}), 1);
  while (1) {
    ht_clear(&new);
    for (size_t i = 0; i < beam.count; ++i) {
      Vector2 *p = beam.items[i];
      size_t nx = p->x, ny = p->y + 1;
      u64 *pc = ht_get(&beam, *p);
      if (!ma_inbounds(&G, nx, ny)) continue;
      if (*ma_at(&G, nx, ny) != '^') {
        Vector2 np = {.x = p->x, .y = p->y + 1};
        u64 *c = ht_get(&new, np);
        if (c) (*c) += *pc;
        else ht_insert(&new, np, *pc);
      } else { /* Split */
        part1++;
        if (ma_inbounds(&G, nx + 1, p->y + 1)) {
          Vector2 np = {.x = p->x + 1, .y = p->y + 1};
          u64 *c = ht_get(&new, np);
          if (c) (*c) += *pc;
          else ht_insert(&new, np, *pc);
        }
        if (ma_inbounds(&G, nx - 1, p->y + 1)) {
          Vector2 np = {.x = p->x - 1, .y = p->y + 1};
          u64 *c = ht_get(&new, np);
          if (c) (*c) += *pc;
          else ht_insert(&new, np, *pc);
        }
      }
    }
    if (new.count == 0) break;
    swap(beam, new);
  }

  printf("part1 = %ld\n", part1);
  u64 part2 = 0;
  for (size_t i = 0; i < beam.count; ++i) {
    u64 *c = ht_get(&beam, *beam.items[i]);
    part2 += *c;
  }
  printf("part2 = %ld\n", part2);
}
