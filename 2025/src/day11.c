#include "libpj.h"
#define PART2

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Device;

#ifdef TEST
#define N 10
#else
#define N 604
#endif

size_t fft, dac;
size_t traverse(Device ds[N], size_t s, size_t f) {
  int c = 0;
  for (size_t i = 0; i < ds[s].count; ++i) {
    if (ds[s].items[i] == f) {
      c++;
      continue;
    }
    c += traverse(ds, ds[s].items[i], f);
  }

  return c;
}

typedef struct {
  size_t fftdac;
  size_t count;
} State;

State visited[N];
size_t traverse2(Device ds[N], size_t s, size_t f, int n, int *c) {
  if (ds[s].items[0] == f) {
    if (n == 0b11) {
      *c += 1;
    }
    return 0;
  }

  for (size_t i = 0; i < ds[s].count; ++i) {
    traverse2(ds, ds[s].items[i], f, n | (ds[s].items[i] == fft ? 1 : 0) | (ds[s].items[i] == dac ? 2 : 0), c);
  }
  if (s == fft) return 1;
  if (s == dac) return 2;

  return 0;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  String2Int indicies = {0};
  Device devices[N] = {0};

  size_t you = 0, svr = 0, out = 0;
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
      da_append(&devices[ii], jj);
    }
  }
  printf("part1 = %zu\n", traverse(devices, you, out));

  int n = 0;
  memset(visited, 0, sizeof(visited));
  traverse2(devices, svr, out, 0, &n);
  printf("part2 = %d\n", n);
}
