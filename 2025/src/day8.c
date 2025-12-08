#include "libpj.h"
#define PART1

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

u64 pow(u64 x, int y) {
  if (y == 0) return 1;

  return (abs(x) * pow(x, y - 1));
}

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

int sort_distance(const void* a, const void* b) {
  const Distance *da = a;
  const Distance *db = b;

  if (da->d < db->d) return -1;

  if (da->d == db->d) return 0;

  return 1;
}

Vector32Int v2i = {0};
Circuits cs = {0};
Distances ds = {0};

void join_circuits(size_t ci, Circuit *a, Circuit *b) {
  for (size_t j = 0; j < b->count; ++j) {
    da_append(a, b->items[j]);
    size_t *cib = ht_get(&v2i, b->items[j]);
    join_circuits(ci, a, &cs.items[*cib]);
    *cib = ci;
  }
  b->count = 0;
}


int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');
  char *line;

  sb_foreach_line(&sb, line) {
    u64 x,y,z;
    expect(sscanf(line, "%ld,%ld,%ld", &x, &y, &z) == 3);
    Circuit c = {0};
    da_append(&c, ((Vector3){x,y,z}));
    da_append(&cs, c);
    ht_insert(&v2i, c.items[0], cs.count - 1);
  }


  for (size_t i = 0; i < cs.count; ++i) {
    for (size_t j = 0; i != j && j < cs.count; ++j) {
      Distance d = {
        .d = v3_distance(cs.items[i].items[0], cs.items[j].items[0]),
        .a = cs.items[i].items[0],
        .b = cs.items[j].items[0]
      };
      da_append(&ds, d);
    }
  }
  da_sort(&ds, sort_distance);

  Circuits ncs = {0};
  for (size_t i = 0; i < 2; ++i) {
    Distance d = ds.items[i];
    size_t ci = *(size_t*)ht_get(&v2i, d.a);
    printf("%zu\n", ci);
    Circuit *ca = &cs.items[ci];
    Circuit cb = cs.items[*(size_t*)ht_get(&v2i, d.b)];
    for (size_t j = 0; j < cb.count; ++j) {
      da_append(ca, cb.items[j]);
      *(size_t*)ht_get(&v2i, cb.items[j]) = ci;
    }
  }
  asm("int3");
}
