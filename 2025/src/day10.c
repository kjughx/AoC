#include "libpj.h"
#include "lp_lib.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

typedef struct {
  size_t indicator;
  struct {
    size_t *items;
    size_t count;
    size_t capacity;
  } s;
} Machine;

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Array;

typedef struct {
  Machine *items;
  size_t count;
  size_t capacity;
} Machines;

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
  PQ *npq = Box(((PQ){.s = s, .n = n, .next = NULL, .prev = NULL}));

  while (n > it->n && it->next) it = it->next;
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
    for (size_t i = 0; i < m->s.count; ++i) {
      if (IS_SET(it->pressed, i)) continue;
      if (it->n + 1 >= min) continue;
      if ((it->s ^ m->s.items[i]) == m->indicator) {
        return it->n + 1;
      }

      PQ *new = pq_insert(&pq, it->s ^ m->s.items[i], it->n + 1);
      new->pressed = it->pressed;
      SETBIT(new->pressed, i);
    }

    pq_remove(&pq, it);
  }

  return min;
}

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Button;

typedef struct {
  Button *items;
  size_t count;
  size_t capacity;
} Buttons;

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Counts;

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');
  size_t part1 = 0;
  size_t part2 = 0;

  Machines ms = {0};
  for (size_t i = 0; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    String_Split sp = sb_split(&line, ' ');
    Machine m = {0};
    size_t ind = 0;
    Buttons bs = {0};
    Counts cs = {0};

    line.items[line.count - 2] = '\0';
    for (size_t j = 1; j < sp.items[0].size - 1; ++j) {
      if (sp.items[0].buf[j] == '#') SETBIT(ind, j-  1);
    }
    m.indicator = ind;
    size_t j;
    for (j = 1; j < sp.count - 1; ++j) {
      if (sp.items[j].buf[0] == '{') break;
      size_t s = 0;
      Button b = {0};
      for (size_t k = 1; k < sp.items[j].size - 1; ++k) {
        if (sp.items[j].buf[k] == ',') continue;
        SETBIT(s, sp.items[j].buf[k] - '0');
        da_append(&b, sp.items[j].buf[k] - '0');
      }
      da_append(&m.s, s);
      da_append(&bs, b);
    }
    char *p = strtok(sp.items[j].buf + 1, ",");
    do {
      da_append(&cs, atoi(p));
      p = strtok(NULL, ",");
    } while (p);

#ifdef PART1
    part1 += dfs(&m);
#endif

#ifdef PART2
  lprec *lp;
  lp = make_lp(0, bs.count);
  set_verbose(lp, 0);
  expect(lp != NULL);

  double *objective = malloc(sizeof(double) * (bs.count + 1));
  objective[0] = 0;
  for (size_t e = 1; e < bs.count + 1; ++e) {
    objective[e] = 1;
  }
  set_obj_fn(lp, objective);
  set_minim(lp);

  for (size_t e = 0; e < cs.count; ++e) {
    double *cfs = malloc(sizeof(double) * (bs.count + 1));
    memset(cfs, 0, sizeof(double) * (bs.count + 1));
    for (size_t k = 0; k < bs.count; ++k) {
      for (size_t l = 0; l < bs.items[k].count; ++l) {
        if (bs.items[k].items[l] == e) {
          cfs[k + 1] = 1;
          break;
        }
      }
    }
    add_constraint(lp, cfs, EQ, cs.items[e]);
    set_int(lp, e + 1, TRUE);
    set_lowbo(lp, e + 1, 0);
  }

  print_lp(lp);
  expect(solve(lp) == 0);

  double *solution = malloc(sizeof(double) * bs.count);
  get_variables(lp, solution);
  for (size_t k = 0; k < bs.count; ++k) {
    part2 += solution[k];
  }
#endif
  }
  printf("part1 = %lu\n", part1);
  printf("part2 = %lu\n", part2);
}
