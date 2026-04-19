# 1855. Maximum Distance Between a Pair of Values
# https://leetcode.com/problems/maximum-distance-between-a-pair-of-values/

from typing import List

class Solution:
    def maxDistance(self, nums1: List[int], nums2: List[int]) -> int:
        j = 0
        for i, v in enumerate(nums1):
            while i+j < len(nums2) and nums2[i+j] >= v:
                j += 1

        return j-1 if j > 0 else 0

    def maxDistanceAlternative(self, nums1: List[int], nums2: List[int]) -> int:
        i, j = 0, 0
        max_distance = 0

        while i < len(nums1) and j < len(nums2):
            if nums1[i] > nums2[j]:
                i += 1
            else:
                max_distance = max(max_distance, j - i)
                j += 1

        return max_distance
