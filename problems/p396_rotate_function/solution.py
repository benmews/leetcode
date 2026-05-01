# 396. Rotate Function
# https://leetcode.com/problems/rotate-function/

from typing import List


class Solution:
    def maxRotateFunction(self, nums: List[int]) -> int:
        n = len(nums)
        sumOfNums = sum(nums)
        maxVal = sum([x * y for x, y in zip(nums, range(n))])
        value = maxVal
        for num in nums:
            value += num * n - sumOfNums
            if value > maxVal:
                maxVal = value
        return maxVal
