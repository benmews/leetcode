# 3761. Minimum Absolute Distance Between Mirror Pairs
# https://leetcode.com/problems/minimum-absolute-distance-between-mirror-pairs/

from typing import List


class Solution:
    def minMirrorPairDistance(self, nums: List[int]) -> int:
        minDist = float('inf');
        prev = {};
        for j, v in enumerate(nums):
            if v in prev:
                dist = abs(prev[v] - j);
                minDist = dist if dist < minDist else minDist;
            prev[self.reverse(v)] = j;
        if minDist == float('inf'):
            return -1;
        return minDist;

    def reverse(self, num: int) -> int:
        return int(str(num)[::-1])