#include "libpj.h"
#include <math.h>
#define PART2

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif
#define INF 100000

typedef struct {
  Vector2 *items;
  size_t count;
  size_t capacity;
} Polygon;

typedef struct {
  Vector2 start;
  Vector2 end;
} Line;

bool lines_intersect(Line* l1, Line *l2) {
    // Calculate the coefficients of the line equations
  Vector2 p1 = l1->start;
  Vector2 p2 = l1->end;
  Vector2 p3 = l2->start;
  Vector2 p4 = l2->end;

  int a1 = p2.y - p1.y;
  int b1 = p1.x - p2.x;
  int a2 = p4.y - p3.y;
  int b2 = p3.x - p4.x;

  int determinant = a1 * b2 - a2 * b1;
  print(determinant);

  return determinant != 0;
}

bool is_inside(Polygon *pg, Vector2 p) {
  int c = 0;
  for (size_t i = 0; i < pg->count; ++i) {
    Vector2 a = pg->items[i];
    Vector2 b = pg->items[(i + 1) % pg->count];
    ssize_t min,max;

    if (a.x == b.x) {
      min = MIN(a.y, b.y);
      max = MAX(a.y, b.y);
      /* Trace a ray to the right, does it intersect? */
      if (p.x <= a.x && min < p.y && p.y <= max) {
        if (p.x == a.x) return true; /* If it's on the line, that counts */
        c++;
      }
    } else if (a.y == b.y) {
      min = MIN(a.x, b.x);
      max = MAX(a.x, b.x);
      if (p.y == a.y && min <= p.x && p.x <= max) return true; /* On the line */
    }
  }
  return c % 2;
}

void print_rect(Polygon *big, Polygon *small) {
  Grid G = {.nx = 12, .ny = 12};
  ma_init(&G);
  ma_fill(&G, '.');
  for (size_t i = 0; i < big->count; ++i) {
    *ma_at(&G, big->items[i].x - 1, big->items[i].y -1 ) = '#';
  }
  for (size_t i = 0; i < small->count; ++i) {
    *ma_at(&G, small->items[i].x - 1, small->items[i].y - 1) = 'O';
  }
  for (size_t y = 0; y < G.ny; ++y) {
    for (size_t x = 0; x < G.nx; ++x) {
      printf("%c", *ma_at(&G, x, y));
    }
    printf("\n");
  }
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  Polygon pg = {0};
  sb_foreach_line(&sb, line) {
    u64 x,y;
    expect(sscanf(line, "%ld,%ld", &x, &y) == 2);
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
  printf("part1 = %lu\n", part1);

/* Counter clockwise? */
  u64 part2 = 0;
  for (size_t i = 0; i < pg.count; ++i) {
    for (size_t j = 0; i != j && j < pg.count; ++j) {
      Vector2 A = pg.items[i];
      Vector2 C = pg.items[j];
      Vector2 B = (Vector2){.x = C.x, .y = A.y};
      Vector2 D = (Vector2){.x = A.x, .y = C.y};
      u64 xx = A.x > C.x ? A.x - C.x : C.x - A.x;
      u64 yy = A.y > C.y ? A.y - C.y : C.y - A.y;
      u64 area = (xx + 1) * (yy + 1);
      if (area > part2 &&
          (is_inside(&pg, A) && is_inside(&pg, B) && is_inside(&pg, C) && is_inside(&pg, D))) {
          part2 = area;
      }
    }
  }

#ifdef TEST
  Grid G = {.nx = 15, .ny = 10};
  ma_init(&G);
  ma_fill(&G, '.');
  for (size_t i = 0; i < pg.count; ++i) {
    *ma_at(&G, pg.items[i].x, pg.items[i].y) = '#';
  }

  for (size_t x = 0; x < G.nx; ++x) {
    for (size_t y = 0; y < G.ny; ++y) {
      if (is_inside(&pg, (Vector2){x, y})) {
        if (*ma_at(&G, x, y) != '#') *ma_at(&G, x, y) = 'O';
      }
    }
  }
  for (size_t y = 0; y < G.ny; ++y) {
    for (size_t x = 0; x < G.nx; ++x) {
      printf("%c", *ma_at(&G, x, y));
    }
    printf("\n");
  }
#endif
  printf("part2 = %ld\n", part2);
}
/* 4733094760 too high */
/* 4605538168 wrong */
/* 1682024932 wrong */
