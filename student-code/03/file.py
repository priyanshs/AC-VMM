class Solution:
    def maximumProduct(self, a: List[int]) -> int:
        a.sort(reverse=True)
        v1=a[0]*a[1]*a[2]
        v2=a[0]*a[-1]*a[-2]
        return max(v1,v2)