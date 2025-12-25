#include "libpj.h"
#include <math.h>

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

typedef struct {
  Vector3 *items;
  size_t count;
  size_t capacity;
} Circuit;

typedef struct {
  Circuit *items;
  size_t count;
  size_t capacity;
} Circuits;

typedef struct {
  u64 d;
  Vector3 a, b;
} Distance;

typedef struct {
  Distance *items;
  size_t count;
  size_t capacity;
} Distances;

u64 v3_distance(Vector3 v1, Vector3 v2) {
  i64 d = pow(v1.x - v2.x, 2) + pow(v1.y - v2.y, 2) + pow(v1.z - v2.z, 2);
  expectf(d > 0, "%ld", d);
  return (u64)d;
}

int sort_distance(const void *a, const void *b) {
  const Distance *da = a;
  const Distance *db = b;

  if (da->d < db->d)
    return -1;

  if (da->d == db->d)
    return 0;

  return 1;
}

Vector32Int v2i = {0};
Circuits cs = {0};
Distances ds = {0};

void join_circuits(size_t ci, Circuit *a, Circuit *b) {
  for (size_t j = 0; j < b->count; ++j) {
    da_append(a, b->items[j]);
    size_t *cib = ht_get(&v2i, b->items[j]);
    *cib = ci;
  }
  b->count = 0;
}

u64 count_circuits() {
  u64 res = 0;
  for (size_t i = 0; i < cs.count; ++i) {
    if (cs.items[i].count)
      res++;
  }
  return res;
}

int sort_circuits(const void *a, const void *b) {
  const Circuit *ca = a;
  const Circuit *cb = b;
  if (ca->count < cb->count)
    return -1;
  if (ca->count == cb->count)
    return 0;
  return 1;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  sb_foreach_line(&sb, line) {
    u64 x, y, z;
    expect(sscanf(line, "%ld,%ld,%ld", &x, &y, &z) == 3);
    Circuit c = {0};
    da_append(&c, ((Vector3){x, y, z}));
    da_append(&cs, c);
    ht_insert(&v2i, c.items[0], cs.count - 1);
  }

  for (size_t i = 0; i < cs.count; ++i) {
    for (size_t j = 0; i != j && j < cs.count; ++j) {
      Distance d = {.d =
                        v3_distance(cs.items[i].items[0], cs.items[j].items[0]),
                    .a = cs.items[i].items[0],
                    .b = cs.items[j].items[0]};
      da_append(&ds, d);
    }
  }
  da_sort(&ds, sort_distance);

#ifdef PART1
  for (size_t i = 0; i < 1000; ++i) {
    Distance d = ds.items[i];
    size_t cia = *(size_t *)ht_get(&v2i, d.a);
    size_t cib = *(size_t *)ht_get(&v2i, d.b);
    if (cia == cib)
      continue;
    join_circuits(cia, &cs.items[cia], &cs.items[cib]);
  }
  da_sort(&cs, sort_circuits);
  u64 part1 = 1;
  for (size_t i = 1; i <= 3; ++i) {
    part1 *= cs.items[cs.count - i].count;
  }
  printf("%lu\n", part1);
#endif

#ifdef PART2
  for (size_t i = 0;; ++i) {
    Distance d = ds.items[i];
    size_t cia = *(size_t *)ht_get(&v2i, d.a);
    size_t cib = *(size_t *)ht_get(&v2i, d.b);
    if (cia == cib)
      continue;
    join_circuits(cia, &cs.items[cia], &cs.items[cib]);
    if (count_circuits() == 1) {
      printf("%ld\n", d.a.x * d.b.x);
      break;
    }
  }
#endif
}
