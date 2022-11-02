def reachNumber(target):
    target = abs(target)
    n = int(math.ceil((math.sqrt(8 * target + 1) - 1) / 2)) # solve inequation: n * (n + 1) / 2 >= target
    d = n * (1 + n) // 2 - target
    if d % 2 == 0:
        # diff is even, always can flip a number from positive to negative
        return n
    else:
        # diff is odd, add more to make diff even, two condition:
        # 2: (1, -2, 3)
        # n = 2, 1 + 2 = 3, diff = 1, next n is 3, we can add 3 and flip one previous number, so only need extra 1 op
        # 5: (1, 2, 3, 4, -5)
        # n = 3, 1 + 2 + 3 = 6, diff = 1, add 4, 5, diff = 10, flip 5 to -5, done, two extra op
        return n + n % 2 + 1