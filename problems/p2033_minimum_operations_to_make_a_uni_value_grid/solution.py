# 2033. Minimum Operations to Make a Uni-Value Grid
# https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/

from typing import List


class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        flat = [v for row in grid for v in row]
        same = all(v % x == flat[0] % x for v in flat)
        length = len(flat)
        average = sum(flat)/length
        flat.sort()
        target = flat[len(flat) // 2]  # median
        ops = sum([abs(v-target) / x for v in flat])
        return int(ops) if same else -1