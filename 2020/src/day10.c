#include "libpj.h"

int sort_int(const void *a, const void *b) {
  return *(int*)a - *(int*)b;
}

da_decl(Adapters, int);

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;
  Adapters aps = {0};

  da_append(&aps, 0);
  sb_foreach_line(&sb, line) {
    da_append(&aps, atoi(line));
  }
  da_sort(&aps, &sort_int);
  da_append(&aps, (aps.items[aps.count - 1] + 3));
  int is[3] = {0};
  for (size_t i = 1; i < aps.count; ++i) {
    assert((aps.items[i + 1] - aps.items[i]) < 4);
    size_t ii = aps.items[i] - aps.items[i - 1];
    is[ii - 1] += 1;
  }
  printf("%d\n", is[0] * is[2]);

  uint64_t *counts = malloc(aps.count * sizeof(uint64_t));
  memset(counts, 0, aps.count * sizeof(uint64_t));
  counts[aps.count - 1] = 1;

  for (ssize_t i = aps.count - 2; i >= 0; --i) {
    int j = 1;
    printf("%d:\n", aps.items[i]);
    while (i + j < (ssize_t)aps.count && ((aps.items[i + j] - aps.items[i]) < 4)) {
      printf("\t%d -> %d = %lu\n", aps.items[i], aps.items[i + j], counts[i + j]);
      counts[i] += counts[i + j];
      j++;
    }
    printf("= %lu\n", counts[i]);
  }
  printf("%lu\n", counts[0]);
}
