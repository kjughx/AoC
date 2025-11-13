#include <cstdlib>
#include <unistd.h>
#include <unordered_map>
#include <string>
#include <iostream>
#include <fstream>
#include <deque>
#include <assert.h>

#define MONKEY_COUNT 2000
static inline long int add(long int a, long int b){ return a + b; }
static inline long int sub(long int a, long int b){ return a - b; }
static inline long int mult(long int a, long int b){ return a * b; }
static inline long int divi(long int a, long int b){ return a / b; }

typedef struct Monkey Monkey;
struct Monkey {
    long int value = 0;
    long int (*op)(long int a, long int b) = NULL;
    Monkey *m1;
    Monkey *m2;
    bool hasValue = false;
    bool hadValue = false;
};

static long int yell(Monkey *monkey) {
    if (!monkey->hasValue){
        assert(monkey->op);
        monkey->value = monkey->op(yell(monkey->m1), yell(monkey->m2));
        monkey->hasValue = true;
    }
    return monkey->value;
}

static void reset(std::unordered_map<std::string, Monkey*> monkeys) {
    for (auto const& [name, monkey]: monkeys) {
        monkey->hasValue = monkey->hadValue;
    }
}

int main(void) {
    std::unordered_map<std::string, Monkey*> monkeys;
    std::ifstream infile("input");

    std::string line;
    std::string name;
    while (std::getline(infile, line)) {
        name = line.substr(0, 4);
        Monkey *monkey;
        if (monkeys.find(name) == monkeys.end()) {
            monkey = (Monkey*) malloc(sizeof(Monkey));
            monkeys.insert(std::pair<std::string, Monkey*>(name, monkey));
        } else {monkey = monkeys.at(name); }

        if (line.size() > 9) {
            name = line.substr(6, 4);
            Monkey *m1;
            if (monkeys.find(name) == monkeys.end()) {
                m1 = (Monkey*) malloc(sizeof(Monkey));
                monkeys.insert(std::pair<std::string, Monkey*>(name, m1));
            } else {m1 = monkeys.at(name);}
            switch (line[11]) {
                case '+': monkey->op = add; break;
                case '-': monkey->op = sub; break;
                case '*': monkey->op = mult; break;
                case '/': monkey->op = divi; break;
            }

            name = line.substr(13, 4);
            Monkey *m2;
            if (monkeys.find(name) == monkeys.end()) {
                m2 = (Monkey*) malloc(sizeof(Monkey));
                monkeys.insert(std::pair<std::string, Monkey*>(name, m2));
            } else {m2 = monkeys.at(name);}

            monkey->m1 = m1;
            monkey->m2 = m2;
        } else  {
            monkey->value = stol(line.substr(6, line.size()));
            monkey->hasValue = true;
            monkey->hadValue = true;
        }
    }

    /* Part 1 */
    printf("root: %ld\n", yell(monkeys.at("root")));


    /* Part 2 */
    long int n = 1000000000000;
    monkeys.at("humn")->value = n;
    long int right = yell(monkeys.at("qwqj"));
    long int left = yell(monkeys.at("fflg"));

    long int add = 1000000000000;
    while (left != right) {
        n += add;
        monkeys.at("humn")->value = n;
        reset(monkeys);
        left = yell(monkeys.at("fflg"));
        if (left < right){
            n -= add;
            add /= 10;
        }
    }
    printf("humn: %ld\n", n);
    /* Answer: 3087390115721 */


    for (auto &monkey: monkeys) {
        free(monkey.second);
    }
}
