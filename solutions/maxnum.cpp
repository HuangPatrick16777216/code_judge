#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> s;
    int n;

    std::cin >> n;
    for (auto i = 0; i < n; i++) {
        int tmp;
        std::cin >> tmp;
        s.push_back(tmp);
    }

    std::cout << *std::max_element(s.begin(), s.end()) << std::endl;
}