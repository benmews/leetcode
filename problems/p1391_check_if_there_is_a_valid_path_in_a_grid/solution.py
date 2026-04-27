# 1391. Check if There is a Valid Path in a Grid
# https://leetcode.com/problems/check-if-there-is-a-valid-path-in-a-grid/

from typing import List


class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        n, m = len(grid), len(grid[0])
        visited = [[False] * m for _ in range(n)]
        directions = ((0, 1), (1, 0), (-1, 0), (0, -1))
        

        def in_bounds(ni: int, nj: int) -> bool:
            return 0 <= ni < n and 0 <= nj < m
        
        def suitingStreetLayout(x, y, current_type):
            has_same_type = grid[x][y] == current_type
            return has_same_type
        
        def can_visit(ni: int, nj: int, current_type: int) -> bool:
            return in_bounds(ni, nj) and not visited[ni][nj] and suitingStreetLayout(ni, nj, current_type)


        def dfs(i, j):
            visited[i][j] = True
            if i == n - 1 and j == m - 1:
                return True

            current_type = grid[i][j]
            nexts = [
                (i + di, j + dj)
                for di, dj in directions
                if can_visit(i + di, j + dj, current_type)
            ]

            return any(dfs(ni, nj) for ni, nj in nexts)

        return dfs(0, 0)
