#include <iostream>
#include <vector>

int search(std::vector<int> nums, int q, int start, int end) {
    if (end-start <= 2) {
        if (nums[start] == q) return start;
        else return start+1;
    }

    int mid = (end+start) / 2;
    if (nums[mid] > q) return search(nums, q, start, mid);
    else return search(nums, q, mid, end);
}

int main() {
    std::vector<int> nums, queries;
    int len, num_q;

    std::cin >> len >> num_q;
    for (auto i = 0; i < len; i++) {
        int tmp;
        std::cin >> tmp;
        nums.push_back(tmp);
    }
    for (auto i = 0; i < num_q; i++) {
        int tmp;
        std::cin >> tmp;
        queries.push_back(tmp);
    }

    for (auto q: queries) {
        std::cout << search(nums, q, 0, len) << std::endl;
    }
}
