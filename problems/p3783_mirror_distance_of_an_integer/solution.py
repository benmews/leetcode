# 3783. Mirror Distance of an Integer
# https://leetcode.com/problems/mirror-distance-of-an-integer/

class Solution:
    def mirrorDistance(self, n: int) -> int:
        rev = int(str(n)[::-1]);
        return abs(n-rev);
