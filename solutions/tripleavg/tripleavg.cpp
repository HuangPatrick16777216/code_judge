#include <iostream>
#include <vector>

int main() {
    std::vector<float> nums;
    int n;

    std::cin >> n;
    for (auto i = 0; i < n; i++) {
        float tmp;
        std::cin >> tmp;
        nums.push_back(tmp);
    }

    while (nums.size() > 1) {
        std::vector<float> new_nums;
        for (auto i = 0; i < nums.size()-1; i++) {
            new_nums.push_back((nums[i]+2*nums[i+1]) / 3);
        }
        nums = new_nums;
    }

    std::cout << (int)nums[0] << std::endl;
}
