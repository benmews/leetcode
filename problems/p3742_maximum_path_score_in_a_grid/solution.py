# 3742. Maximum Path Score in a Grid
# https://leetcode.com/problems/maximum-path-score-in-a-grid/

from typing import List

class Solution:
    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        n = len(grid)
        m = len(grid[0])
        dirs = ((0,1), (1,0))
        current = [(0,0,0,0)] # (x,y,cost,score)
        next = []

        while current not empty:
            for cell in current:
                for dir in dirs:   
                    newX = cell[0]+dir[0]
                    newY = cell[1]+dir[1]
                    if newX < n and newY < m:
                        cost = 1 if grid[newX][newY] > 0 else 0
                        next.append((newX, newY,cell[2]+cost,cell[3]+grid[newX][newY]))
                current.remove(cell)
            # merge fields with same x y here

            # if there are contents of current with x=n-1 and y=m-1, then return the one with highest score here

            current = next
            next = []

        return -1