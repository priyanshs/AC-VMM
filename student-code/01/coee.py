class Solution(object):
    def maximumProduct(self, nums):
        x=sorted(nums)
        a = x[0]*x[1]*x[-1]
        b=x[-1]*x[-2]*x[-3]
        return max(a,b)
        
