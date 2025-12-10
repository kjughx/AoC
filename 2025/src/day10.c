#include "libpj.h"
#define PART1

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
} Schematics;

typedef struct {
  size_t indicator;
  Schematics s;
} Machine;

typedef struct {
  Machine *items;
  size_t count;
  size_t capacity;
} Machines;

typedef struct {
  size_t s;
  size_t n;
} State;

typedef struct _PQ PQ;
struct _PQ  {
  size_t s;
  size_t n;
  size_t pressed;
  PQ *next;
  PQ *prev;
};

PQ *pq_insert(PQ **head, size_t s, size_t n) {
  PQ *it = *head;

  while (n > it->n && it->next) it = it->next;
  PQ *npq = Box(((PQ){.s = s, .n = n, .next = NULL, .prev = NULL}));
  /* Insert `npq` after `it` */
  if (it->next)
    it->next->prev = npq;

  npq->next = it->next;
  it->next = npq;
  npq->prev = it;

  return npq;
}

void pq_remove(PQ **head, PQ *pq) {
  if (pq == *head) {
    assert(pq->prev == NULL);
    *head = pq->next;
  }

  if (pq->next) pq->next->prev = pq->prev;
  if (pq->prev) pq->prev->next = pq->next;
}

size_t dfs(Machine *m) {
  size_t min = m->s.count;
  PQ *pq = Box(((PQ){0}));

  for (PQ *it = pq; it; it = it->next) {
    if (it->s == m->indicator) {
      return it->n;
    }

    for (size_t i = 0; i < m->s.count; ++i) {
      if (IS_SET(it->pressed, i)) continue;
      if (it->n + 1 >= min) continue;

      PQ *new = pq_insert(&pq, it->s ^ m->s.items[i], it->n + 1);
      new->pressed = it->pressed;
      SETBIT(new->pressed, i);
    }

    pq_remove(&pq, it);
  }

  return min;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  Machines ms = {0};
  for (size_t i = 0; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    String_Split sp = sb_split(&line, ' ');
    Machine m = {0};
    size_t ind = 0;
    for (size_t j = 1; j < sp.items[0].size - 1; ++j) {
      if (sp.items[0].buf[j] == '#') SETBIT(ind, j-  1);
    }
    m.indicator = ind;
    for (size_t j = 1; j < sp.count - 1; ++j) {
      if (sp.items[j].buf[0] == '{') break;
      size_t s = 0;
      for (size_t k = 1; k < sp.items[j].size - 1; ++k) {
        if (sp.items[j].buf[k] == ',') continue;
        SETBIT(s, sp.items[j].buf[k] - '0');
      }
      da_append(&m.s, s);
    }
    da_append(&ms, m);
  }

  u64 part1 = 0;
  for (size_t i = 0; i < ms.count; ++i) {
    size_t n = part1(&ms.items[i]);
    part1 += n;
    printf("%zu: %zu\n", i, n);
  }
  printf("part1 = %lu\n", part1);
}
