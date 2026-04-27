# 1559. Detect Cycles in 2D Grid
# https://leetcode.com/problems/detect-cycles-in-2d-grid/

from typing import Any


class Solution:
    def containsCycle(self, grid: Any) -> bool:
        n, m = len(grid), len(grid[0])
        visited = [[False] * m for _ in range(n)]

        def dfs(i, j, pi, pj):
            if visited[i][j]:
                return True;
            visited[i][j] = True;
            nexts = [(i+di, j+dj) for (di, dj) in [(0,1),(1,0),(-1,0),(0,-1)] if 0 <= i+di < n and 0 <= j+dj < m and (i+di, j+dj) != (pi,pj) and grid[i+di][j+dj] == grid[i][j]]
            
            for ni, nj in nexts:
                if dfs(ni,nj, i, j):
                    return True;
            return False;

        for i in range(n):
            for j in range(m):
                if not visited[i][j] and dfs(i,j,-1,-1):
                    return True;
        return False;