# 3742. Maximum Path Score in a Grid
# https://leetcode.com/problems/maximum-path-score-in-a-grid/

from typing import List


class Solution:
    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        n = len(grid)
        m = len(grid[0])
        dirs = ((0, 1), (1, 0))
        current = {(0, 0): {0: 0}}

        def prune_frontier(cost_to_score: dict[int, int]) -> dict[int, int]:
            pruned: dict[int, int] = {}
            best_score = -1

            for cost in sorted(cost_to_score):
                score = cost_to_score[cost]
                if score > best_score:
                    pruned[cost] = score
                    best_score = score

            return pruned

        for _ in range(n + m - 2):
            next_states: dict[tuple[int, int], dict[int, int]] = {}

            for (x, y), cost_map in current.items():
                for cost, score in cost_map.items():
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if nx >= n or ny >= m:
                            continue

                        new_cost = cost + (1 if grid[nx][ny] > 0 else 0)
                        if new_cost > k:
                            continue

                        new_score = score + grid[nx][ny]
                        bucket = next_states.setdefault((nx, ny), {})
                        bucket[new_cost] = max(bucket.get(new_cost, -1), new_score)

            current = {
                cell: prune_frontier(cost_map)
                for cell, cost_map in next_states.items()
            }

        end_scores = current.get((n - 1, m - 1), {})
        return max(end_scores.values(), default=-1)