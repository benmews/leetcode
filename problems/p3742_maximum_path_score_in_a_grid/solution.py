# 3742. Maximum Path Score in a Grid
# https://leetcode.com/problems/maximum-path-score-in-a-grid/

from typing import List

class Solution:
    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        n = len(grid)
        m = len(grid[0])
        dirs = ((0,1), (1,0))

        def dfs(i, j, usedk, score):

            if i<0 or j <0 or i>=n or j>=m:
                return -1
            newk = usedk+1 if grid[i][j] > 0 else usedk+0

            if newk > k:
                return -1

            newScore = score + grid[i][j]

            if i == n-1 and j == m-1:
                return newScore
            
            highestContinuation = []
            for dir in dirs:
                highestContinuation.append(dfs(i+dir[0], j+dir[1], newk, newScore))

            return max(highestContinuation)
        
        return dfs(0,0, 0, 0)