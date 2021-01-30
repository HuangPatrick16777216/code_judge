#include <iostream>

int main() {
    int steps;
    float pos, target, step, range;

    steps = 0;
    std::cin >> pos >> target >> step >> range;
    while (true) {
        if (abs(pos-target) <= range) {
            std::cout << steps << std::endl;
            break;
        }
        if (pos < target) {
            while (pos < target-range) {
                pos += step;
                steps++;
            }
        } else {
            while (pos > target+range) {
                pos -= step;
                steps++;
            }
        }
        step /= 2;
    }
}
