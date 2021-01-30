pos, target, step, target_range = map(int, input().strip().split())
steps = 0
while True:
    if abs(pos-target) <= target_range:
        print(steps)
        break
    if pos < target:
        while pos < target-target_range:
            pos += step
            steps += 1
    else:
        while pos > target+target_range:
            pos -= step
            steps += 1
    step /= 2
