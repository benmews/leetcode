# 1848. Minimum Distance to the Target Element
# https://leetcode.com/problems/minimum-distance-to-the-target-element/

from typing import List


class Solution:
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        index = -1;
        for i, v in enumerate(nums):
            if v == target:
                if abs(i-start) < abs(index-start) or index == -1:
                    index = i;
        return abs(index-start);