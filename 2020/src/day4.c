#include "libpj.h"

static const char* FIELDS[] = {
  "byr",
  "iyr",
  "eyr",
  "hgt",
  "hcl",
  "ecl",
  "pid",
  "cid",
};

typedef struct {
  char *key;
  char* value;
} Field;

typedef struct {
  Field *items;
  size_t count;
  size_t capacity;

  bool has_cid;
} Passport;

typedef struct {
  Passport *items;
  size_t count;
  size_t capacity;
} Passports;

static inline bool is_hex(char *h) {
  expect(h);
  size_t l = strlen(h);
  if (l != 7) return false;

  for (size_t i = 1; i < l; ++i) {
    int c = (int)h[i];
    if (97 <= c && c <= 102) continue;
    if (48 <= c && c <= 57) continue;
    return false;
  }

  return true;
}

int main(void) {
  String_Builder sb = {0};
  sb_read_file(&sb, stdin);
  String_Split lines = sb_split(&sb, '\n');

  Passports ps = {0};
  Passport p = {0};
  for (size_t i = 0; i < lines.count; ++i) {
    String_Builder line = sv_to_sb(lines.items[i]);
    if (lines.items[i].size == 0) {
      da_append(&ps, p);
      memset(&p, 0, sizeof(p));
      continue;
    }
    String_Split fields = sb_split(&line, ' ');
    for (size_t j = 0; j < fields.count; ++j) {
      Field f = {
        .key = strndup(fields.items[j].buf, 3),
        .value = strndup(fields.items[j].buf + 4, fields.items[j].size - 4),
      };
      if (strcmp(f.key, "cid") == 0) p.has_cid = true;
      if (strcmp(f.key, "byr") == 0) {
        int y = atoi(f.value);
        if (!(1920 <= y && y <= 2002)) continue;
      }
      if (strcmp(f.key, "iyr") == 0) {
        int y = atoi(f.value);
        if (!(2010 <= y && y <= 2020)) continue;
      }
      if (strcmp(f.key, "eyr") == 0) {
        int y = atoi(f.value);
        if (!(2020 <= y && y <= 2030)) continue;
      }
      if (strcmp(f.key, "hgt") == 0) {
        int hgt = 0;
        char unit[2];
        sscanf(f.value, "%d%s", &hgt, unit);
        if (strcmp(unit, "cm") == 0) {
          if (!(150 <= hgt && hgt <= 193)) continue;
        } else {
          if (!(59 <= hgt && hgt <= 76)) continue;
        }
      }
      if (strcmp(f.key, "hcl") == 0) {
        if (!is_hex(f.value)) continue;
      }
      if (strcmp(f.key, "ecl") == 0) {
        char *valid[] = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"};
        bool is_valid = false;
        for (size_t k = 0; k < ARRAY_LEN(valid); ++k) {
          if (strcmp(f.value, valid[k]) == 0) {
            is_valid = true;
            break;
          }
        }
        if (!is_valid) continue;
      }
      if (strcmp(f.key, "pid") == 0) {
        if (strlen(f.value) != 9) continue;
        if (atoi(f.value) == 0) continue;
      }
      da_append(&p, f);
    }
  }
  da_append(&ps, p);

  int ans = 0;
  for (size_t i = 0; i < ps.count; ++i) {
    if (ps.items[i].count == ARRAY_LEN(FIELDS) ||
        (ps.items[i].count == ARRAY_LEN(FIELDS) - 1 && !ps.items[i].has_cid)) ans++;
  }

  printf("%d\n", ans);
}
