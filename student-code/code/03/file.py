def reachNumber(target):
    target = abs(target)
    
    def reachable(i):
        return (i + 1) * i // 2
    
    left, right = 0, target * 2
    while left + 1 < right:            
        mid = (left + right) // 2         
        if reachable(mid) >= target:
            right = mid
        else:
            left = mid
            
    if reachable(left) >= target:              
        while reachable(left) % 2 != target % 2:
            left += 1 
        return left
    if reachable(right) >= target:
        while reachable(right) % 2 != target % 2:
            right += 1             
        return right