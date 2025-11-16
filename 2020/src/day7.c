#include "libpj.h"

typedef struct {
  const char* color;
  size_t count;
} Tuple;

typedef struct Bag {
  Tuple *items;
  size_t count;
  size_t capacity;
} Bag;

typedef struct BagNode {
  const char* key;
  Bag value;

  struct BagNode *next;
} BagNode;

typedef struct {
  BagNode *items[TABLE_SIZE];
} Bags;

String2Int visited = {0};
int count_bags1(Bags *bags, const char* key, int *count) {
  struct _node *vis = NULL;
  ht_get(&visited, key, vis);
  if (vis) {
    return *count;
  }
  ht_insert(&visited, key, 0);
  if (strcmp(key, "shiny gold") != 0) (*count)++;

  BagNode *n;
  ht_get(bags, key, n);
  Bag *bag = &n->value;
  for (size_t i = 0; i < bag->count; ++i) {
    *count = count_bags1(bags, bag->items[i].color, count);
  }

  return *count;
}

int count_bags2(Bags *bags, const char *key) {
  struct _node *vis = NULL;
  ht_get(&visited, key, vis);
  if (vis) {
    return vis->value;
  }

  BagNode *n;
  ht_get(bags, key, n);
  Bag *bag = &n->value;
  if (bag->count == 0) return 0;
  int count = 0;

  for (size_t i = 0; i < bag->count; ++i) {
    count += bag->items[i].count * (1 + count_bags2(bags, bag->items[i].color));
    ht_insert(&visited, key, count);
  }

  return count;
}


int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  Bags bags = {0};
  Bags reverse = {0};
  BagNode *n;
  char *tmp;
  for (size_t l = 0; l < lines.count; ++l) {
    String_Builder line = sv_to_sb(lines.items[l]);
    tmp = line.items;
    sb_skip_word(&line);
    sb_skip_word(&line);
    char *color = strndup(tmp, line.items - tmp - 1);
    ht_get(&reverse, color, n);
    if (!n) {
      ht_insert(&reverse, color, ((Bag){0}));
    }

    if (strcmp(line.items, "bags contain no other bags.") == 0) {
      ht_insert(&bags, color, ((Bag){0}));
      continue;
    }

    sb_skip_word(&line);
    sb_skip_word(&line);

    Bag bag = {0};
    while(*line.items) {
      int count = atoi(line.items);
      sb_skip_word(&line);

      tmp = line.items;
      sb_skip_word(&line);
      sb_skip_word(&line);
      char *_color = strndup(tmp, line.items - tmp - 1);
      sb_skip_word(&line);
      da_append(&bag, ((Tuple){.color = _color, .count = count}));

      ht_get(&reverse, _color, n);
      if (!n) {
        ht_insert(&reverse, _color, ((Bag){0}));
      }

      ht_get(&reverse, _color, n);
      Bag *_bag = &n->value;
      da_append(_bag, ((Tuple){.color = strdup(color)}));
    }
    ht_insert(&bags, color, bag);
  }

  int ans = 0;
  printf("%d\n", count_bags1(&reverse, "shiny gold", &ans));

  memset(&visited, 0, sizeof(String2Int));
  ans = 0;
  printf("%d\n", count_bags2(&bags, "shiny gold"));
}
