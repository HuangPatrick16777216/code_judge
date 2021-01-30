#include <iostream>
#include <vector>
using namespace std;

int solution(vector<float> nums) {
    if (nums.size() == 1) return nums[0];
    vector<float> new_nums;
    for (auto i = 0; i < nums.size()-1; i++) {
        new_nums.push_back((nums[i]+2*nums[i+1]) / 3);
    }
    return solution(new_nums);
}

int main() {
    vector<float> nums;
    int n;

    cin >> n;
    for (auto i = 0; i < n; i++) {
        float tmp;
        cin >> tmp;
        nums.push_back(tmp);
    }

    cout << solution(nums) << endl;
}
