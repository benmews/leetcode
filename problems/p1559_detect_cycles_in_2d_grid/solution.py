# 1559. Detect Cycles in 2D Grid
# https://leetcode.com/problems/detect-cycles-in-2d-grid/

from typing import Any


class Solution:
    def containsCycle(self, grid: Any) -> bool:
        m, n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)]

        def dfs(i: int, j: int, pi: int, pj: int) -> bool:
            if visited[i][j]:
                return True

            visited[i][j] = True
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == grid[i][j] and (ni != pi or nj != pj):
                    if dfs(ni, nj, i, j):
                        return True

            return False

        for i in range(m):
            for j in range(n):
                if not visited[i][j] and dfs(i, j, -1, -1):
                    return True

        return False