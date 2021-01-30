input()
nums = list(map(int, input().strip().split()))
while len(nums) > 1:
    new_nums = []
    for i in range(len(nums)-1):
        new_nums.append((nums[i]+2*nums[i+1]) / 3)
    nums = new_nums

print(int(nums[0]))
