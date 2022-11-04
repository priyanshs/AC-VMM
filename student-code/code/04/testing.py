from math import ceil,sqrt

def reachNumber(target):
    target = abs(target)
    n = ceil(sqrt(2*target)-1) # n = 1 gives O(sqrt(target)) solution
    while True:
        upper = n * (n+1) // 2
        if upper >= target and (upper - target) % 2 == 0:
            break
        n += 1
    return n