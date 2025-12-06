#include "libpj.h"

typedef struct {
  u64 *items;
  size_t count;
  size_t capacity;
} Values;

typedef struct {
  char *items;
  size_t count;
  size_t capacity;
} Operators;

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');
  char *line;

  Operators ops = {0};
  Values vs = {0};
  sb_foreach_line(&sb, line) {
    char *b = line;
    while (*b && (isdigit(*b) || isspace(*b))) {
      if (isdigit(*b)) {
        da_append(&vs, atol(b));
        while (isdigit(*b)) b++;
      }
      while (isspace(*b)) b++;
    }
    while (*b && !isdigit(*b)) {
      if (!isdigit(*b)) {
        da_append(&ops, *b);
        b++;
      }
      while (isspace(*b)) b++;
    }
  }
  u64 part1 = 0;
  for (size_t i = 0; i < 1000; ++i) {
    u64 res = ops.items[i] == '+' ? 0 : 1;
    for (size_t j = 0; j < 4; ++j) {
      if (ops.items[i] == '+') res += vs.items[j * 1000 + i];
      if (ops.items[i] == '*') res *= vs.items[j * 1000 + i];
    }
    part1 += res;
  }
  printf("%ld\n", part1);

  /* Longest line */
  ssize_t p = 0;
  for (size_t i = 0; i < lines.count - 1; ++i) {
    p = MAX(p, (ssize_t)lines.items[i].size);
  }
  u64 part2 = 0;
  vs.count = 0;
  while (--p >= 0) {
    u64 value = 0;
    for (size_t i = 0; i < lines.count - 1; ++i) {
      if (isdigit(lines.items[i].buf[p])) {
        int v = lines.items[i].buf[p] - '0';
        value = value * 10 + v;
      }
    }
    if (value > 0) da_append(&vs, value);

    if (lines.items[lines.count - 2].buf[p] == '+' || lines.items[lines.count - 2].buf[p] == '*') {
      char op = lines.items[lines.count - 2].buf[p];
      u64 res = op == '+' ? 0 : 1;
      for (size_t i = 0; i < vs.count; ++i) {
        if (op == '+') res += vs.items[i];
        if (op == '*') res *= vs.items[i];
      }
      part2 += res;
      vs.count = 0;
    }
  }
  printf("%ld\n", part2);
}
