#include "libpj.h"

#if defined(PART1) && defined(PART2)
#error "Define either PART1 or PART2, not both"
#endif
#if !defined(PART1) && !defined(PART2)
#error "Define either PART1 or PART2"
#endif

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  u64 ans = 0;
  for (size_t i = 0; i < lines.count; ++i) {
    u64 s,e;
    const char *line = sv_to_cstr(lines.items[i]);
    expect(sscanf(line, "%ld-%ld", &s, &e) == 2);

    for (u64 j = s; j <= e; ++j) {
      char *ss = strdup(format("%ld", j));
      size_t l = strlen(ss);
#ifdef PART1
      if (l % 2 != 0) continue;
      if (strncmp(ss, ss + l / 2, l / 2) == 0) {
        ans += j;
      }
#endif

#ifdef PART2
      for (size_t k = 1; k < l; ++k) {
        if (l % k != 0) continue;
        char *needle = strndup(ss, k);

        int c = 0;
        for (size_t m = 0; m < l; m += k) {
          if (strncmp(ss + m, needle, k) == 0) c++;
        }

        if (c == l / k) {
          ans += j;
          break;
        }
      }
#endif
    }
  }
    printf("%ld\n", ans);
}
