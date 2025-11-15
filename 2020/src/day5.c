#include "libpj.h"

#define ROWS 128

typedef struct {
  int *items;
  size_t count;
  size_t capacity;
} Ids;

typedef struct {
  int *items;
  size_t count;
  size_t capacity;
} Row;


int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;
  Ids ids = {0};

  int max_id = 0;

  Row rows[ROWS] = {0};
  sb_foreach_line(&sb, line) {
    int max = ROWS - 1;
    int min = 0;
    size_t l = strlen(line);
    for (size_t i = 0; i < l - 3; ++i) {
      if (line[i] == 'F') {
        int d = max - min;
        max -= d / 2 + (d % 2 == 0 ? 0 : 1);
      }
      if (line[i] == 'B') {
        int d = max - min;
        min += d / 2 + (d % 2 == 0 ? 0 : 1);
      }
    }
    int row = max;

    max = 7;
    min = 0;
    for (size_t i = l - 3; i < l; ++i) {
      if (line[i] == 'L') {
        int d = max - min;
        max -= d / 2 + (d % 2 == 0 ? 0 : 1);
      }
      if (line[i] == 'R') {
        int d = max - min;
        min += d / 2 + (d % 2 == 0 ? 0 : 1);
      }
    }
    int col = max;
    int id = row * 8 + col;

    if (id > max_id) max_id = id;
    da_append(&rows[row], col);
  }
  for (size_t i = 0; i < ROWS; ++i) {
    Row row = rows[i];
    if (row.count != 8) {
      for (size_t j = 0; j < row.count; ++j) {
        /* Check what is missing and calculate by hand */
        printf("%zu %d\n", i, row.items[j]);
      }
    }
  }
}
