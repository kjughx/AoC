#include "libpj.h"

#define matches(s1, s2) ((strcmp((s1), (s2)) == 0))
#define matches_n(s1, s2, n) ((strncmp((s1), (s2), (n)) == 0))

#define PART2

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

typedef struct {
  char *r;
  int arg;
} Instruction;

typedef struct {
  Instruction *items;
  size_t count;
  size_t capacity;
} Instructions;

void find_replace(Instructions *is) {
  bool *visited = malloc(is->count * sizeof(bool));
  bool swapped = false;
  bool looped = false;
  bool looping = false;
  String2Int loop = {0};
  struct _node *l;

  size_t ip = 0;
  while (ip < is->count) {
    Instruction ins = is->items[ip];
    if (visited[ip] && !looped) {
      looping = true;
    }
    visited[ip] = true;

    if (looping) {
      ht_get(&loop, ins.r, l);
      if (!l) ht_insert(&loop, ins.r, 0)
      else {
        looping = false;
        looped = true;
      }
    }

    if (matches_n(ins.r, "jmp", 3)) {
      if (looped && !swapped) {
        ht_get(&loop, is->items[ip + 1].r, l);
        if (!l) { /* The next instruction is not part of the loop */
          swapped = true;
          memcpy(ins.r, "nop", 3);
          return;
        }
      }
      ip += ins.arg;
      continue;
    }
    /* what about 'nop'? :( */
    if (matches_n(ins.r, "nop", 3)) {}
    if (matches_n(ins.r, "acc", 3)) {}

    ip++;
  }
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  Instructions is = {0};
  for (size_t l = 0; l < lines.count; ++l) {
    String_View line = lines.items[l];
    char *r = strndup(line.buf, line.size);
    line.buf += 3;
    int arg = atoi(line.buf);
    da_append(&is, ((Instruction){.r = r, .arg = arg}));
  }

#ifdef PART2
  find_replace(&is);
#endif

  size_t ip = 0;
  int acc = 0;
  bool *visited = malloc(is.count * sizeof(bool));
  memset(visited, 0, is.count * sizeof(bool));
  while (ip < is.count) {
    Instruction ins = is.items[ip];

#ifdef PART1
    if (visited[ip]) break;
#endif
    visited[ip] = true;

    if (matches_n(ins.r, "nop", 3)) {}
    if (matches_n(ins.r, "jmp", 3)) {
      ip += ins.arg;
      continue;
    }
    if (matches_n(ins.r, "acc", 3)) {
      acc += ins.arg;
    }

    ip++;
  }
  printf("%d\n", acc);
}
