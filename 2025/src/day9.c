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
  Vector2 A, B;
  Vector2 min, max;
} Rect;

typedef struct {
  Vector2 p1, p2;
} Line;

Vector2 inside = {0};

bool line_intersect(Line l1, Line l2) {
    // Calculate the coefficients of the lines
    double a1 = l1.p2.y - l1.p1.y;
    double b1 = l1.p1.x - l1.p2.x;
    double c1 = a1 * l1.p1.x + b1 * l1.p1.y;

    double a2 = l2.p2.y - l2.p1.y;
    double b2 = l2.p1.x - l2.p2.x;
    double c2 = a2 * l2.p1.x + b2 * l2.p1.y;

    // Calculate the determinant
    double det = a1 * b2 - a2 * b1;

    // If the determinant is zero, the lines are parallel
    if (det == 0) {
        return false;
    }

    // Calculate the intersection point
    double x = (b2 * c1 - b1 * c2) / det;
    double y = (a1 * c2 - a2 * c1) / det;
    if ((x == l2.p1.x || x == l2.p2.x) && (y == l2.p1.y || y == l2.p2.y)) return false;

    // Check if the intersection point lies on both line segments
    if ((x >= MIN(l1.p1.x, l1.p2.x) && x <= MAX(l1.p1.x, l1.p2.x) && y >= MIN(l1.p1.y, l1.p2.y) && y <= MAX(l1.p1.y, l1.p2.y)) &&
        (x >= MIN(l2.p1.x, l2.p2.x) && x <= MAX(l2.p1.x, l2.p2.x) && y >= MIN(l2.p1.y, l2.p2.y) && y <= MAX(l2.p1.y, l2.p2.y))) {
      return true;
    }

    return false;
}

#define rect(a, b) {.A = (a), .B = (b),                     \
    .min = {.x = MIN((a).x, (b).x), .y = MIN((a).y, (b).y)},  \
    .max = {.x = MAX((a).x, (b).x), .y = MAX((a).y, (b).y)}}

typedef struct {
  Rect *items;
  size_t count;
  size_t capacity;
} Rects;

bool rect_overlap(Rect *r, Rect *e) {
  return !(r->max.x <= e->min.x ||
           e->max.x <= e->min.x ||
           r->max.y <= e->min.y ||
           e->max.y <= e->min.y);
}

/* https://www.engr.colostate.edu/~dga/documents/papers/point_in_polygon.pdf */
double winding(Polygon *pg, Vector2 p) {
  double w = 0;

  for (size_t i = 0; i < pg->count; ++i) {
    Vector2 a = pg->items[i];
    Vector2 b = pg->items[(i + 1) % pg->count];

    Vector2 va = {.x = a.x - p.x, .y = a.y - p.y};
    Vector2 vb = {.x = b.x - p.x, .y = b.y - p.y};

    /* Point on segment? */
    if (va.y * vb.y == 0) { /* Horizontal */
      if (va.x * vb.x <= 0) return true;
    }
    if (va.x * vb.x == 0) { /* Vertical */
      if (va.y * vb.y <= 0) return true;
    }

    if (va.y * vb.y < 0) {
      double r = va.x + va.y * (vb.x - va.x) / (float)(va.y - vb.y);
      if (r > 0) {
        if (va.y < 0) w += 1.0f;
        else          w -= 1.0f;
      }
    } else if (va.y == 0 && va.x > 0) {
      if (vb.y > 0) w += (1.0f / 2);
      else          w -= (1.0f / 2);
    } else if (vb.y == 0 && vb.x > 0) {
      if (va.y < 0) w += (1.0f / 2);
      else          w -= (1.0f / 2);
    }
  }

  return w;
}

/* ssize_t min, max; */
/* bool is_inside(Polygon *pg, Vector2 p) { */
/*   return winding(pg, p) != 0; */
/* } */

/* bool is_inside(Polygon *pg, Vector2 p) { */
/*   int c = 0; */
/*   for (size_t i = 0; i < pg->count; ++i) { */
/*     Vector2 a = pg->items[i]; */
/*     Vector2 b = pg->items[(i + 1) % pg->count]; */
/*     ssize_t min,max; */

/*     if (a.x == b.x) { */
/*       min = MIN(a.y, b.y); */
/*       max = MAX(a.y, b.y); */
/*       /\* Trace a ray to the right, does it intersect? *\/ */
/*       if (p.x <= a.x && min < p.y && p.y <= max) { */
/*         if (p.x == a.x) return true; /\* If it's on the line, that counts *\/ */
/*         c++; */
/*       } */
/*     } else if (a.y == b.y) { */
/*       min = MIN(a.x, b.x); */
/*       max = MAX(a.x, b.x); */
/*       if (p.y == a.y && min <= p.x && p.x <= max) return true; /\* On the line *\/ */
/*     } */
/*   } */
/*   return c % 2; */
/* } */

bool is_inside(Polygon *pg, Vector2 p) {
  for (size_t i = 0; i < pg->count; ++i) {
    Vector2 a = pg->items[i];
    Vector2 b = pg->items[(i + 1) % pg->count];
    if (line_intersect((Line){a, b}, (Line){inside, p})) return false;
    /*   ssize_t min, max; */
    /*   if (a.x == b.x && p.x == b.x) { */
    /*     min = MIN(a.y, b.y); */
    /*     max = MAX(a.y, b.y); */
    /*     if (!(min <= p.x && p.x <= max)) return false; */
    /*   } else if (a.y = b.y && p.y == b.y) { */
    /*     min = MIN(a.x, b.x); */
    /*     max = MAX(a.x, b.x); */
    /*     if (!(min <= p.y && p.y <= max)) return false; */
      /* } */

    /* } */
  }
  return true;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  Polygon pg = {0};
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
  printf("part1 = %lu\n", part1);

  inside.x = (pg.items[0].x + pg.items[1].x) / 2;
  inside.y = (pg.items[0].x + pg.items[1].y) / 2;


/* Counter clockwise? */
/*   u64 part2 = 0; */

/*   Rects edges = {0}; */
/*   for (size_t i = 0; i < pg.count; ++i) { */
/*     Vector2 a = pg.items[i]; */
/*     Vector2 b = pg.items[(i + 1) % pg.count]; */
/*     Rect e = { */
/*       .A = a, */
/*       .B = b, */
/*       .min = {.x = MIN(a.x, b.x), .y = MIN(a.y, b.y)}, */
/*       .max = {.x = MAX(a.x, b.x), .y = MAX(a.y, b.y)}, */
/*     }; */
/*     da_append(&edges, e); */
/*   } */
/*   for (size_t i = 0; i < pg.count; ++i) { */
/*     for (size_t j = 0; i != j && j < pg.count; ++j) { */
/*       Vector2 A = pg.items[i]; */
/*       Vector2 C = pg.items[j]; */
/*       Vector2 B = (Vector2){.x = C.x, .y = A.y}; */
/*       Vector2 D = (Vector2){.x = A.x, .y = C.y}; */

/*       u64 area = (ABS(A.x - C.x) + 1) * (ABS(A.y - C.y) + 1); */
/*       Rect r = rect(A, C); */
/*       bool overlaps = false; */
/*       for (size_t k = 0; k < edges.count; ++k) { */
/*         if (rect_overlap(&r, &edges.items[k])) overlaps = true; */
/*       } */
/*       if (!overlaps) part2 = MAX(area, part2); */
/*     } */
/*   } */
/*   /\* for (size_t i = 0; i < pg.count; ++i) { *\/ */
/*   /\*   for (size_t j = 0; i != j && j < pg.count; ++j) { *\/ */
/*   /\*     Vector2 A = pg.items[i]; *\/ */
/*   /\*     Vector2 C = pg.items[j]; *\/ */
/*   /\*     Vector2 B = (Vector2){.x = C.x, .y = A.y}; *\/ */
/*   /\*     Vector2 D = (Vector2){.x = A.x, .y = C.y}; *\/ */

/*   /\*     u64 area = (ABS(A.x - C.x) + 1) * (ABS(A.y - C.y) + 1); *\/ */

/*   /\*     A.x += SIGN(B.x - A.x); *\/ */
/*   /\*     B.x -= SIGN(B.x - A.x); *\/ */
/*   /\*     C.x -= SIGN(B.x - A.x); *\/ */
/*   /\*     D.x += SIGN(B.x - A.x); *\/ */

/*   /\*     A.y += SIGN(D.y - A.y); *\/ */
/*   /\*     B.y -= SIGN(D.y - A.y); *\/ */
/*   /\*     C.y -= SIGN(D.y - A.y); *\/ */
/*   /\*     D.y += SIGN(D.y - A.y); *\/ */

/*   /\*     /\\* u64 xx = A.x > C.x ? A.x - C.x : C.x - A.x; *\\/ *\/ */
/*   /\*     /\\* u64 yy = A.y > C.y ? A.y - C.y : C.y - A.y; *\\/ *\/ */
/*   /\*     /\\* u64 area = (xx + 1) * (yy + 1); *\\/ *\/ */
/*   /\*     if (area > part2 && *\/ */
/*   /\*         (is_inside(&pg, A) && is_inside(&pg, B) && is_inside(&pg, C) && is_inside(&pg, D))) { *\/ */
/*   /\*         part2 = area; *\/ */
/*   /\*     } *\/ */
/*   /\*   } *\/ */
/*   /\* } *\/ */

/* #ifdef TEST */
  Grid G = {.nx = 15, .ny = 10};
  ma_init(&G);
  ma_fill(&G, '.');
  for (size_t i = 0; i < pg.count; ++i) {
    *ma_at(&G, pg.items[i].x, pg.items[i].y) = '#';
  }

  for (size_t x = 0; x < G.nx; ++x) {
    for (size_t y = 0; y < G.ny; ++y) {
      /* double w = winding(&pg, (Vector2){x, y}); */
      /* if (w == 1.0f) *ma_at(&G, x, y) = 'O'; */
      /* else if (w == 0.5) *ma_at(&G, x, y) = 'P'; */
      /* else if (w == -0.5) *ma_at(&G, x, y) = 'N'; */
      /* if (is_inside(&pg, (Vector2){x, y})) *ma_at(&G, x, y) = 'O'; */
      if (is_inside(&pg, (Vector2){x, y}))
        if (*ma_at(&G, x, y) != '#') *ma_at(&G, x, y) = 'O';
    }
  }
  *ma_at(&G, inside.x, inside.y) = 'X';
  for (size_t y = 0; y < G.ny; ++y) {
    for (size_t x = 0; x < G.nx; ++x) {
      printf("%c", *ma_at(&G, x, y));
    }
    printf("\n");
  }
  printf("%d\n", line_intersect((Line){4, 9}, Line l2)
/* #endif */
/*   printf("part2 = %ld\n", part2); */
}
/* 4733094760 too high */
/* 4605266710 wrong */
/* 4605538168 wrong */
/* 3184727672 wrong */
/* 1682024932 wrong */
