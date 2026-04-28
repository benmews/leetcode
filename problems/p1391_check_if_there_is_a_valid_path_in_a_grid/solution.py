# 1391. Check if There is a Valid Path in a Grid
# https://leetcode.com/problems/check-if-there-is-a-valid-path-in-a-grid/

from typing import List


class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        n, m = len(grid), len(grid[0])
        visited = [[False] * m for _ in range(n)]
        directions = ((0, 1), (1, 0), (-1, 0), (0, -1))
        layouts = {
            1: ((0, -1), (0, 1)),
            2: ((-1, 0),(1, 0)),
            3: ((0, -1),(1, 0)),
            4: ((0, 1),(1, 0)),
            5: ((0, -1),(-1, 0)),
            6: ((0, 1),(-1, 0)),
        }

        def in_bounds(ni: int, nj: int) -> bool:
            return 0 <= ni < n and 0 <= nj < m
        
        def suitingLayout(i, j, di, dj):
            current_layout = layouts[grid[i][j]]
            next_layout = layouts[grid[i+di][j+dj]]

            return (di, dj) in current_layout and (-di, -dj) in next_layout
        
        def can_visit(i: int, j: int, di: int, dj: int) -> bool:
            return (
                in_bounds(i+di, j+dj) 
                and not visited[i+di][j+dj] 
                and suitingLayout(i, j, di, dj)
                )

        def dfs(i, j):
            visited[i][j] = True
            if i == n - 1 and j == m - 1:
                return True

            nexts = [
                (i + di, j + dj)
                for di, dj in directions
                if can_visit(i, j, di, dj)
            ]

            return any(dfs(ni, nj) for ni, nj in nexts)

        return dfs(0, 0)
