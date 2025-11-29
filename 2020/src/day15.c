#include "libpj.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

#define CACHE_SIZE 10000

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);

  Int2Int numbers = {};
  sb_strip(&sb, '\n');
  String_Split start = sb_split(&sb, ',');
  u64 turn;
  u64 prev;
  u64 i;
  u64 val;
  u64 cache[CACHE_SIZE] = {0};
  for (i = 0; i < start.count; ++i) {
    turn = i + 1;
    val = atoi(sv_to_cstr(start.items[i]));
    ht_insert(&numbers, val, turn);
    cache[val] = turn;
  }
  prev = val;

  for (; i < 30000000; ++i) {
    if (i % 100000 ==0) printf("%d\n", i);
    turn = i + 1;
    val = prev;

    if (val < CACHE_SIZE && cache[val] > 0) {
      prev = turn - 1 - cache[val];
      cache[val] = turn - 1;
      continue;
    }

    u64 *last_turn = ht_get(&numbers, prev);
    if (last_turn) {
      prev = (turn - 1) - *last_turn;
      *last_turn = turn - 1;
    } else {
      ht_insert(&numbers, prev, turn - 1);
      prev = 0;
    }
  }
  printf("%zu: %zu\n", turn, prev);
}
