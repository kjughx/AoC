#include "libpj.h"

#ifdef TEST
#define PREAMBLE 5
#else
#define PREAMBLE 25
#endif

typedef struct {
  int *items;
  size_t count;
  size_t capacity;
} List;

bool is_valid(int n, List pa) {
  expect(pa.count == PREAMBLE);
  for (size_t i = 0; i < PREAMBLE; ++i) {
    for (size_t j = 0; j < PREAMBLE; ++j) {
      if (pa.items[i] + pa.items[j] == n) return true;
    }
  }

  return false;
}

int cont_sum(size_t mm, size_t mx, List lst) {
  int v = 0;
  for (size_t i = mm; i <= mx; ++i) {
    v += lst.items[i];
  }
  return v;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  size_t i = 0;
  List pa = {0};
  List lst = {0};
  for (i = 0; i < lines.count; ++i) {
    if (i < PREAMBLE) da_append(&pa, atoi(sv_to_cstr(lines.items[i])));
    da_append(&lst, atoi(sv_to_cstr(lines.items[i])));
  }

  int invalid;
  for (i = PREAMBLE; i < lst.count; ++i) {
    if (!is_valid(lst.items[i], pa)) {
      invalid = lst.items[i];
      break;
    }
    pa.items++;
    pa.count--;
    da_append(&pa, lst.items[i]);
  }

  printf("Invalid = %d\n", invalid);
  size_t mm = 0, mx = 1;

  while (1) {
    int v = cont_sum(mm, mx, lst);
    if (v == invalid) break;
    if (v > invalid) {
      mm++;
      mx = mm + 1;
    }
    if (v < invalid) mx++;
  }

  int min = 100000000;
  int max = 0;
  for (size_t i = mm; i <= mx; ++i) {
    if (lst.items[i] < min) min = lst.items[i];
    if (lst.items[i] > max) max = lst.items[i];
  }
  printf("%d\n", min + max);
}
