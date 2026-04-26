# 2615. Sum of Distances
# https://leetcode.com/problems/sum-of-distances/

from typing import List


class Solution:
    def distance(self, nums: List[int]) -> List[int]:
        groups = {}
        for i, v in enumerate(nums):
            if v not in groups:
                groups[v] = []
            groups[v].append(i)

        result = [0] * len(nums)
        for indexes in groups.values():
            k = len(indexes)
            prefix = 0
            suffix = sum(indexes)
            for j, idx in enumerate(indexes):
                suffix -= idx
                result[idx] = j * idx - prefix + suffix - (k - 1 - j) * idx
                prefix += idx

        return result