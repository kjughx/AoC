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
  char *line;

  sb_foreach_line(&sb, line) {
    printf("%s\n", line);
  }
}
