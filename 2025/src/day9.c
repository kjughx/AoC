#include "libpj.h"

typedef struct {
  Vector2 *items;
  size_t count;
  size_t capacity;
} Points;

#define N 100000

bool is_inside(Vector2 rs[N], Vector2 ps[4]) {
  for (size_t i = 0; i < 4; ++i) {
    Vector2 p0 = ps[i];
    Vector2 p1 = ps[(i+1) % 4];

    if (p0.x == p1.x) {
      ssize_t x = p0.x;
      for (ssize_t y = MIN(p0.y, p1.y); y < MAX(p0.y, p1.y); ++y) {
        if (!(rs[y].x <= x && x <= rs[y].y)) return false;
      }
    } else {
      ssize_t y = p0.y;
      for (ssize_t x = MIN(p0.x, p1.x); x < MAX(p0.x, p1.x); ++x) {
        if (!(rs[y].x <= x && x <= rs[y].y)) return false;
      }
    }
  }

  return true;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  Points pg = {0};
  Vector2 rs[N] = {0};
  sb_foreach_line(&sb, line) {
    ssize_t x,y;
    expect(sscanf(line, "%zd, %zd", &x, &y) == 2);
    da_append(&pg, ((Vector2){x,y}));
  }

  u64 part1 = 0;
  for (size_t i = 0; i < pg.count; ++i) {
    for (size_t j = 0; i != j && j < pg.count; ++j) {
      Vector2 a = pg.items[i];
      Vector2 b = pg.items[j];
      u64 xx = a.x > b.x ? a.x - b.x : b.x - a.x;
      u64 yy = a.y > b.y ? a.y - b.y : b.y - a.y;
      u64 area = (xx + 1) * (yy + 1);
      part1 = MAX(area, part1);
    }
  }

  for (size_t i = 0; i < pg.count; ++i) {
    Vector2 p0 = pg.items[i];
    Vector2 p1 = pg.items[(i + 1) % pg.count];
    if (p0.y == p1.y) {
      if (rs[p0.y].x == 0) rs[p0.y].x = MIN(p0.x, p1.x);
      else rs[p0.y].x = MIN(rs[p0.y].x, MIN(p0.x, p1.x));

      if (rs[p0.y].y == 0) rs[p0.y].y = MAX(p0.x, p1.x);
      else rs[p0.y].y = MAX(rs[p0.y].y, MAX(p0.x, p1.x));
    } else {
      for (ssize_t y = MIN(p0.y, p1.y); y < MAX(p0.y, p1.y); ++y) {
        if (rs[y].x == 0) rs[y].x = p0.x;
        else rs[y].x = MIN(rs[y].x, p0.x);

        if (rs[y].y == 0) rs[y].y = p0.x;
        else rs[y].y = MAX(rs[y].y, p0.x);
      }
    }
  }

  u64 part2 = 0;
  for (size_t i = 0; i < pg.count; ++i) {
    for (size_t j = 0; i != j && j < pg.count; ++j) {
        Vector2 p0 = pg.items[i];
        Vector2 p2 = pg.items[j];
        Vector2 p1 = {p0.x, p2.y};
        Vector2 p3 = {p2.x, p0.y};

        u64 area = (ABS(p0.x - p2.x) + 1) * (ABS(p0.y - p2.y) + 1);
        Vector2 corners[] = {p0, p1, p2, p3};
        if (area > part2 && is_inside(rs, corners)) {
        part2 = area;
        }
    }
  }

  printf("part1 = %lu\n", part1);
  printf("part2 = %lu\n", part2);
}
