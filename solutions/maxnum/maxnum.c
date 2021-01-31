#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    scanf("%d", &n);

    int *nums = (int*)malloc(sizeof(int) * n);

    for (int i = 0; i < n; i++) {
        scanf("%d", &nums[i]);
    }

    int max_ind = 0;
    for (int i = 0; i < n; i++) {
        if (nums[i] > nums[max_ind]) max_ind = i;
    }

    printf("%d\n", nums[max_ind]);
    free(nums);
}