# 2078. Two Furthest Houses With Different Colors
# https://leetcode.com/problems/two-furthest-houses-with-different-colors/

from typing import List


class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        coli = colors[0]
        colj = colors[-1]
        for j, v in enumerate(colors):
            if v != colj:
                dist1 = len(colors) - 1 - j
                break
        for i, v in enumerate(reversed(colors)):
            if v != coli:
                dist2 = len(colors) - 1 - i
                break

        return max(dist1, dist2)

    def maxDistanceSlow(self, colors: List[int]) -> int:
        n = len(colors)
        max_distance = 0

        for i in range(n):
            for j in range(i + 1, n):
                if colors[i] != colors[j]:
                    max_distance = max(max_distance, j - i)

        return max_distance
