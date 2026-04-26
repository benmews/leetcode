# 2833. Furthest Point From Origin
# https://leetcode.com/problems/furthest-point-from-origin/

class Solution:
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        wild = moves.count('_')
        left = moves.count('L')
        right = moves.count('R')
        return wild + abs(left - right)
