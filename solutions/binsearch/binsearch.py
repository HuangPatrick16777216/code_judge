def search(nums, q, start=0, end=None):
    if end is None:
        end = len(nums)

    if end - start <= 2:
        return start if nums[start] == q else start+1

    mid = int((end+start) / 2)
    if nums[mid] > q:
        return search(nums, q, start, mid)
    else:
        return search(nums, q, mid, end)

input()
nums = list(map(int, input().strip().split()))
queries = list(map(int, input().strip().split()))
for q in queries:
    print(search(nums, q))
