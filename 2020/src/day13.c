#include "libpj.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

typedef struct {
  int t;
  int offset;
} Timestamp;
typedef struct {
  Timestamp *items;
  size_t count;
  size_t capacity;
} Timestamps;

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  int busid = 0;
  expect(sscanf(sv_to_cstr(lines.items[0]), "%d", &busid) == 1);

  Timestamps ts = {0};
  String_Builder _t = sv_to_sb(lines.items[1]);
  String_Split _ts = sb_split(&_t, ',');

#ifdef PART1
  for (size_t i = 0; i < _ts.count; ++i) {
    if (_ts.items[i].buf[0] != 'x') {
      da_append(&ts, atoi(sv_to_cstr(_ts.items[i])));
    }
  }
  int min = busid;
  int minb = 0;
  printf("busid = %d\n", busid);
  for (size_t i = 0; i < ts.count; ++i) {
    int t = ts.items[i] - busid % ts.items[i];
    if (t < min) {
      min = t;
      minb = ts.items[i];
    }
  }
  print(min * minb);
#endif


  int maxt = 0;
  int maxof = 0;
  for (size_t i = 0; i < _ts.count; ++i) {
    if (_ts.items[i].buf[0] == 'x') continue;

    Timestamp t = {
      .t = atoi(sv_to_cstr(_ts.items[i])),
      .offset= i,
    };

    da_append(&ts, t);
    if (t.t + t.offset > maxt) {
      maxt = t.t;
      maxof = t.offset;
    }
  }

  /* int N = 1068781; */
  /* for (size_t i = 0; i < ts.count; ++i) { */
  /*   Timestamp t = ts.items[i]; */
  /*   printf("%d %d\n", t.t, N % (t.t - t.offset)); */
  /* } */

 /*  int N = 1; */
 /*  for (size_t i = 0; i < ts.count; ++i) { */
 /*    Timestamp t = ts.items[i]; */
 /*    N = N * t.t + t.offset; */
 /*  } */
 /*  printf("%d %d, %lld\n", maxt, maxof, N); */

  long long n = 1;
 next:
  if (n % 100000000 == 0) printf("%lld\n", n * maxt - maxof);
  n += 1;
  int N = n * maxt - maxof;
  for (size_t i = 0; i < ts.count; ++i) {
    Timestamp t = ts.items[i];
    if ((N + t.offset) % t.t != 0) goto next;
  }
  goto next;
  out:
  printf("%ld\n", n * maxt - maxof);
}
