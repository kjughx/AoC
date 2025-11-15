#include "libpj.h"

int part1 = 0;

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  int ans = 0;
  sb_foreach_line(&sb, line) {
    int mm, mx;
    char c;
    char s[1024];
    sscanf(line, "%d-%d %c: %s\n", &mm, &mx, &c, s);

    int count = 0;
#ifdef 0
    for (size_t i = 0; i < strlen(s); ++i) {
        if (s[i] == c) count++;
        if (count > mx) break;
      }
    }
    if (mm <= count && count <= mx) ans++;
#endif
    if ((s[mm - 1] == c) ^ (s[mx - 1] == c)) ans++;
  }
  printf("%d\n", ans);
}
