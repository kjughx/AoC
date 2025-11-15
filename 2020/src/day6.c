#include "libpj.h"

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);

  String_Split lines = sb_split(&sb, '\n');

  Array letters = {0};

  int ans = 0;
  int l = 0;
  for (size_t i = 0; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    l = 0;
    if (lines.items[i].size == 0) {
      int _ans = 0;
#ifdef PART1
      for (size_t j = 0; j < letters.count; ++j) {
        _ans |= letters.items[j];
      }
#endif
      _ans = letters.items[0];
      for (size_t j = 1; j < letters.count; ++j) {
        _ans &= letters.items[j];
      }
      for (size_t j = 0; j < 26; ++j) {
        ans += ((_ans >> j) & 0x01);
      }
      memset(&letters, 0, sizeof(typeof(letters)));
      continue;
    }

    for (size_t j = 0; j < line.count - 1; ++j) {
      l |= (1 << (line.items[j] - 97));
    }
    da_append(&letters, l);
  }

  printf("%d\n", ans);
}
