#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> nums;
    int n;

    cin >> n;
    for (auto i = 0; i < n; i++) {
        int tmp;
        cin >> tmp;
        nums.push_back(tmp);
    }

    cout << *max_element(nums.begin(), nums.end()) << endl;
}