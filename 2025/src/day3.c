#include <math.h>
#include "libpj.h"

#ifdef PART1
#define BANK_LEN 2
#else
#define BANK_LEN 12
#endif

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  char *line;

  u64 ans = 0;
  sb_foreach_line(&sb, line) {
    int arr[BANK_LEN] = {0};
    size_t iarr[BANK_LEN] = {0};
    size_t l = strlen(line);
    for (size_t i = 0; i < BANK_LEN; ++i) {
      for (size_t j = i; j < l - ((BANK_LEN - 1) - i); ++j) {
        int v = line[j] - '0';
        if (v > arr[i] && (i == 0 || j > iarr[i - 1])) {
          arr[i] = v;
          iarr[i] = j;
        }
      }
    }
    u64 v = 0;
    for (size_t i = 0; i < BANK_LEN; ++i) {
      v += pow(10, (BANK_LEN - 1) - i) * arr[i];
    }
    ans += v;
  }

  printf("%ld\n", ans);
}
