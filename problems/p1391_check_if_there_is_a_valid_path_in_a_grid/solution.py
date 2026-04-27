# 1391. Check if There is a Valid Path in a Grid
# https://leetcode.com/problems/check-if-there-is-a-valid-path-in-a-grid/

from typing import List


class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        n, m = len(grid), len(grid[0])
        visited = [[False] * m for _ in range(n)]
        directions = ((0, 1), (1, 0), (-1, 0), (0, -1))
        layouts = {
            1: ('l', 'r'),
            2: ('u','d'),
            3: ('l','d'),
            4: ('r','d'),
            5: ('l','u'),
            6: ('r','u'),
        }

        def in_bounds(ni: int, nj: int) -> bool:
            return 0 <= ni < n and 0 <= nj < m
        
        def suitingLayout(ni, nj, current_layout):
            next_layout = layouts[grid[ni][nj]]
            return bool(set(current_layout) & set(next_layout))
        
        def can_visit(ni: int, nj: int, current_layout) -> bool:
            return in_bounds(ni, nj) and not visited[ni][nj] and suitingLayout(ni, nj, current_layout)


        def dfs(i, j):
            visited[i][j] = True
            if i == n - 1 and j == m - 1:
                return True

            current_layout = layouts[grid[i][j]]
            nexts = [
                (i + di, j + dj)
                for di, dj in directions
                if can_visit(i + di, j + dj, current_layout)
            ]

            return any(dfs(ni, nj) for ni, nj in nexts)

        return dfs(0, 0)
