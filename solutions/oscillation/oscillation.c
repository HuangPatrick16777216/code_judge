#include <stdio.h>

int main() {
    int steps;
    float pos, target, step, range;

    steps = 0;
    scanf("%e %e %e %e", &pos, &target, &step, &range);
    while (1) {
        if (abs(pos-target) <= range) {
            printf("%d\n", steps);
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
