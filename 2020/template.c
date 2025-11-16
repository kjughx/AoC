#include "libpj.h"

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');
  char *line;

  sb_foreach_line(&sb, line) {
    printf("%s\n", line);
  }
}
