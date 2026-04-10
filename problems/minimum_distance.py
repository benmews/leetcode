class Solution:
    def minimum_distance(self, nums):
        if len(nums) < 2:
            return 0

        return min(abs(nums[i] - nums[i - 1]) for i in range(1, len(nums)))
