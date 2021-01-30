def solution(nums):
    if len(nums) == 1:
        return nums[0]
    else:
        new_nums = []
        for i in range(len(nums)-1):
            new_nums.append((nums[i]+2*nums[i+1]) / 3)
        return solution(new_nums)

input()
print(solution(list(map(int, input().strip().split()))))
