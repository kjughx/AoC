#include <cmath>
#include <iostream>
#include <fstream>
#include <string>

#define BASE 5

int main(void) {
    std::ifstream infile("inputs/day25");
    std::string line;
    std::string name;

    const char* to_snafu = "=-012";

    long int number = 0;
    char c;
    while (std::getline(infile, line)) {
        int i = 0;
        while (!(line.empty())) {
            c = line.back();

            switch (c) {
                case '2':
                    number += 2 * std::pow(BASE, i); break;
                case '1':
                    number += 1 * std::pow(BASE, i); break;
                case '0': break;
                case '-':
                    number += -1 * std::pow(BASE, i); break;
                case '=':
                    number += -2 * std::pow(BASE, i); break;
            }
            i++;
            line.pop_back();
        }
    }
    std::cout << number << std::endl;

    /* Now do it in reverse */

    int maxbase = 0;
    int num = 0;
    while (std::pow(BASE, maxbase) < number) { maxbase++; }

    std::cout << maxbase << std::endl;

    std::string output = "";
    int div;
    while (number) {
        div = ((number+2) % 5);
        output = to_snafu[div] + output;
        std::cout << div << std::endl;
        number = (number+2)/5;
    }
    std::cout << output << std::endl;
}

/* Part 1 = 20-==01-2-=1-2---1-0 */
