#include "libpj.h"

typedef struct {
  int *items;
  size_t count;
  size_t capacity;
} Array;

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;
  Array a = {0};

  sb_foreach_line(&sb, line) {
    int aa;
    sscanf(line, "%d", &aa);
    da_append(&a, aa);
  }
  for (size_t i = 0; i < a.count; ++i) {
    for (size_t j = 0; j < a.count; ++j) {
      for (size_t k = 0; k < a.count; ++k) {
        if (a.items[i] + a.items[j] + a.items[k] == 2020) {
          printf("%d\n", a.items[i] * a.items[j] * a.items[k]);
          return 0;
        }
      }
    }
  }

}
