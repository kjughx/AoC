#include "libpj.h"

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Device;

#define N 605

Device ds[N] = {0};
Device dsb[N] = {0};
String2Int indicies = {0};

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Queue;

Int2Int can_reach(size_t n) {
  Queue q = {0};
  Int2Int reachable = {0};
  ht_insert(&reachable, n, 0);
  da_append(&q, n);
  while (q.count > 0) {
    size_t node = da_pop(&q);
    for (size_t i = 0; i < dsb[node].count; ++i) {
      size_t d = dsb[node].items[i];
      if (ht_get(&reachable, d)) continue;
      ht_insert(&reachable, d, 0);
      da_append(&q, d);
    }
  }
  return reachable;
}

size_t traverse(size_t s, size_t f){
  Int2Int reachable = can_reach(f);
  Queue q = {0};
  da_append(&q, s);
  size_t n = 0;
  while (q.count > 0) {
    size_t node = da_pop(&q);
    if (node == f) {
      n++;
      continue;
    }
    if (!ht_get(&reachable, node)) continue;

    for (size_t i = 0; i < ds[node].count; ++i) {
      da_append(&q, ds[node].items[i]);
    }
  }

  return n;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  size_t you, fft, dac, out, svr;
  for (size_t i = 0; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    String_Split words = sb_split(&line, ' ');

    char *start = sv_to_cstr(words.items[0]);
    start[3] = '\0';
    size_t ii;
    size_t *_idx = ht_get(&indicies, start);
    if (!_idx) {
      ii = indicies.count;
      ht_insert(&indicies, start, indicies.count);
    } else ii = *_idx;

    if (strcmp(start, "you") == 0) you = ii;
    if (strcmp(start, "svr") == 0) svr = ii;
    if (strcmp(start, "dac") == 0) dac = ii;
    if (strcmp(start, "fft") == 0) fft = ii;

    for (size_t j = 1; j < words.count; ++j) {
      char *device = sv_to_cstr(words.items[j]);
      size_t jj;
      size_t *_idx = ht_get(&indicies, device);
      if (!_idx) {
        jj = indicies.count;
        ht_insert(&indicies, device, indicies.count);
      } else jj = *_idx;

      if (strcmp(device, "out") == 0) out = jj;
      da_append(&ds[ii], jj);
      da_append(&dsb[jj], ii);
    }
  }

  printf("part1 = %zu\n", traverse(you, out));
  printf("part2 = %zu\n", traverse(svr, fft) * traverse(fft, dac) * traverse(dac, out));
}
