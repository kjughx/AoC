#include "libpj.h"
#define PART1

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

typedef struct {
  /* char *items; */
  bool *items;
  size_t count;
  size_t capacity;
} Indicator;

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Schematic;

typedef struct {
  Schematic *items;
  size_t count;
  size_t capacity;
} Schematics;

typedef struct {
  Indicator in;
  Schematics s;
} Machine;

typedef struct {
  Machine *items;
  size_t count;
  size_t capacity;
} Machines;

/* struct __node_Schematic2Int { */
/*   Schematic *key; */
/*   u64 *value; */
/*   struct __node_Schematic2Int *next; */
/* }; */

/* typedef struct { */
/*   struct __node_Schematic2Int *nodes[TABLE_SIZE]; */

/*   Schematic **items; */
/*   size_t count; */
/*   size_t capacity; */
/* } Schematic2Int; */
/* #undef __hash */
/* #define __hash(__k) hash_schematic(__k) */
/* size_t hash_schematic(Schematic _key) { */
/*   size_t hash = MAGIC; */
/*   int c; */
/*   for (size_t i = 0; i < _key.count; ++i) { */
/*     size_t key = _key.items[i]; */
/*     while ((c = (key & 0xff))) { */
/*       hash = ((hash << 5) + hash) + c; // hash * 33 + c */
/*       key >>= 8; */
/*     } */
/*   } */

/*   return hash; */
/* } */
/* #undef ht_get */
/* #define ht_get(__k) __ht_get_schem((ht), (__k), offsetof(typeof(*(ht)->nodes[0]), key), \ */
/*                                                     offsetof(typeof(*(ht)), nodes), sizeof(*(ht)->nodes), \ */
/*                                                     offsetof(typeof(*(ht)->nodes[0]), value), \ */
/*                                                     offsetof(typeof(*(ht)->nodes[0]), next)) */
/* static inline void *__ht_get_schem(void *ht, Schematic key, size_t key_offset, */
/*                              size_t nodes_offset, size_t node_size, */
/*                              size_t value_offset, size_t next_offset) { */
/*   size_t nodes = (size_t)ht + nodes_offset; // &nodes[0] */
/*   size_t idx = __hash(key) % TABLE_SIZE; */
/*   void *node = *(void **)((size_t)nodes + idx * node_size); // nodes[idx] -> struct node* */
/*   if (node == NULL) return NULL; */

/*   Schematic *_key = NULL; */

/*   /\* Now start searching the linked list, for a node with the same key *\/ */
/*   while (node != NULL) { */
/*     _key = *(Schematic **)((size_t)node + key_offset); */
/*     if (memcmp(key.items, _key->items, MIN(key.count, _key->count)) == 0) break; */
/*     node = *(void **)(((size_t)node) + next_offset); // node->next */
/*   } */

/*   if (node == NULL) return NULL; */

/*   void *p = *(void**)(((size_t)node) + value_offset); // &node->value */
/*   return p; */
/* } */

typedef struct {
  size_t *items;
  size_t count;
  size_t capacity;
} Button2Index;

int sort(const void *a, const void *b) {
  const Button2Index *ba = a;
  const Button2Index *bb = b;
  if (ba->count < bb->count) return -1;
  if (ba->count == bb->count) return 0;
  return 1;
}

int min = 100000000;
int bfs1(Machine *m, Button2Index *b2i, bool* lights, size_t bb, size_t c) {
  Schematic s = m->s.items[b2i->items[bb]];
  c++;
  for (size_t i = 0; i < s.count; ++i) {
    lights[s.items[i]] ^= 1;
  }
  if (memcmp(lights, m->in.items, sizeof(bool) * m->in.count) == 0) return c;
  if (c > min) return c;

  for (size_t i = 0; i < m->in.count; ++i) {
    if (lights[i]) {
      for (size_t j = 0; j < b2i->items[i]; ++j) {
        min = MIN(c, bfs1(m, b2i, lights, j, c));
      }
    }
  }

  return min;
}

int press_buttons(Machine *m) {
  bool *lights = malloc(m->in.count);
  memset(lights, false, sizeof(bool) * m->in.count);

  /* How to press button 1? */
  Button2Index *b2i = malloc(m->in.count * sizeof(Button2Index));
  memset(b2i, 0, m->in.count * sizeof(Button2Index));
  for (size_t i = 0; i < m->s.count; ++i) {
    for (size_t j = 0; j < m->s.items[i].count; ++j) {
      da_append(&b2i[m->s.items[i].items[j]], i);
    }
  }

  for (size_t i = 0; i < m->in.count; ++i) {
    da_sort(&b2i[i], &sort);
  }

  for (size_t i = 0; i < m->in.count; ++i) {
    if (m->in.items[i]) {
      for (size_t j = 0; j < b2i->items[i]; ++j) {
        min = MIN(min, bfs1(m, b2i, lights, i, 0));
      }
    }
  }

  free(lights);
  return min;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');
  char *line;

  Machines ms = {0};
  for (size_t i = 0; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    String_Split sp = sb_split(&line, ' ');
    Machine m = {0};
    for (size_t j = 1; j < sp.items[0].size - 1; ++j) {
      da_append(&m.in, sp.items[0].buf[j] == '#');
    }
    for (size_t j = 1; j < sp.count - 1; ++j) {
      if (sp.items[i].buf[j] == '{') break;
      Schematic s = {0};
      for (size_t k = 1; k < sp.items[j].size - 1; ++k) {
        if (sp.items[j].buf[k] == ',') continue;
        da_append(&s, sp.items[j].buf[k] - '0');
      }
      da_append(&m.s, s);
    }
    da_append(&ms, m);
  }
  printf("%d\n", press_buttons(&ms.items[0]));
  /* for (size_t i = 0; i < ms.count; ++i) { */
  /* } */
}
