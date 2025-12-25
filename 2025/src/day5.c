#include "libpj.h"

typedef struct {
  u64 min, max;
} Range;

typedef struct {
  Range *items;
  size_t count;
  size_t capacity;
} Ranges;

int sort_range(const void *a, const void *b) {
  const Range *ra = a;
  const Range *rb = b;
  if (ra->min == rb->min && ra->max == rb->max)
    return 0;
  if (ra->min < rb->min)
    return -1;
  if (ra->min <= rb->min && ra->max <= rb->max)
    return -1;
  return 1;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  Ranges ranges = {0};
  size_t i;
  for (i = 0; i < lines.count; ++i) {
    String_View line = lines.items[i];
    u64 m1, m2;
    if (line.size == 0)
      break;
    expect(sscanf(sv_to_cstr(line), "%ld-%ld", &m1, &m2) == 2);
    da_append(&ranges, ((Range){.min = m1, .max = m2}));
  }
  da_sort(&ranges, &sort_range);

  i++;
  u64 part1 = 0;
  for (; i < lines.count; ++i) {
    u64 ing = atol(sv_to_cstr(lines.items[i]));
    size_t j;
    bool fresh = false;
    for (j = 0; j < ranges.count; ++j) {
      u64 min = ranges.items[j].min;
      u64 max = ranges.items[j].max;
      if ((min <= ing && ing <= max)) {
        fresh = true;
        break;
      }
    }
    if (fresh) {
      part1++;
    }
  }
  printf("part1 = %lu\n", part1);

  u64 part2 = 0;
  Ranges final = {0};

  Range current = ranges.items[0];
  for (size_t i = 1; i < ranges.count; ++i) {
    if (current.max >= ranges.items[i].min &&
        current.max <= ranges.items[i].max) {
      current.max = ranges.items[i].max;
    } else if (current.min <= ranges.items[i].min &&
               current.max >= ranges.items[i].max) {
      continue;
    } else {
      da_append(&final, current);
      current = ranges.items[i];
    }
  }
  da_append(&final, current);

  for (size_t i = 0; i < final.count; ++i) {
    part2 += final.items[i].max - final.items[i].min + 1;
  }
  printf("part2 = %lu\n", part2);
}
