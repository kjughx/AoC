#include "libpj.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

#define stringify(...) #__VA_ARGS__
#ifdef TEST
#define N_FIELDS 3
#else
#define N_FIELDS 20
#endif


typedef struct {
  char *name;
  u32 min1, max1;
  u32 min2, max2;
} Range;

typedef struct {
  Range *items;
  size_t count;
  size_t capacity;
} Ranges;

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Valid;

bool valid[1000] = {0};

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  size_t i = 0;
  Ranges ranges = {0};
  for (; i < lines.count; ++i) {
    const char *line = sv_to_cstr(lines.items[i]);
    u32 max1, max2, min1, min2;
    char *field = NULL;
    if (lines.items[i].size == 0) break;
    expect(sscanf(line, "%ms %d-%d or %d-%d", &field, &min1, &max1, &min2, &max2) == 5);
    Range r = {.name = field, min1, max1, min2, max2};
    for (size_t j = min1; j <= max1; ++j) valid[j] = true;
    for (size_t j = min2; j <= max2; ++j) valid[j] = true;

    da_append(&ranges, r);
  }
  expect(ranges.count == N_FIELDS);

  i += 5;

  Valid valid_tickets = {0};
  u64 ans = 0;
  for (; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    String_Split values = sb_split(&line, ',');
    size_t j;
    for (j = 0; j < values.count; ++j) {
      u32 value = atoi(sv_to_cstr(values.items[j]));
      if (!valid[value]) {
        ans += value;
        break;
      }
    }
    if (j == values.count) da_append(&valid_tickets, i);
  }
  printf("PART1: %ld\n", ans);

  /* dim0: ticket field, dim1: fields */
  bool fields[N_FIELDS][N_FIELDS];
  memset(fields, true, N_FIELDS * N_FIELDS * sizeof(bool));

  for (size_t i = 0; i < valid_tickets.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[valid_tickets.items[i]]);

    String_Split values = sb_split(&line, ',');
    for (size_t j = 0; j < values.count; ++j) {
      u32 value = atoi(sv_to_cstr(values.items[j]));
      expect(value > 0);
      for (size_t k = 0; k < ranges.count; ++k) {
        Range *r = &ranges.items[k];
        if (!((r->min1 <= value && value <= r->max1) || (r->min2 <= value && value <= r->max2))) {
          fields[j][k] = false;
        }
      }
    }
  }

  int total = 0;
  do {
    total = 0;
    for (size_t i = 0; i < N_FIELDS; ++i) {
      int ans = 0;
      size_t jans = -1;
      size_t ians = -1;
      for (size_t j = 0; j < N_FIELDS; ++j) {
        if (fields[i][j]) {
          ans++;
          jans = j;
          ians = i;
        }
      }
      if (ans == 1) {
        total++;
        for (size_t j = 0; j < N_FIELDS; ++j) {
          if (j != ians) fields[j][jans] = false;
        }
      }
    }
  } while(total < N_FIELDS);

  String_Builder myticket = sv_to_sb(lines.items[22]);
  String_Split values = sb_split(&myticket, ',');
  ans = 1;
  for (size_t i = 0; i < N_FIELDS; ++i) {
    for (size_t j = 0; j < 6; ++j) {
      if (fields[i][j]) {
        ans *= atoi(sv_to_cstr(values.items[i]));
      }
    }
  }
  printf("PART2: %ld\n", ans);
}
