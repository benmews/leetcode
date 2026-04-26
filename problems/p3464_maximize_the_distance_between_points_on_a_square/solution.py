# 3464. Maximize the Distance Between Points on a Square
# https://leetcode.com/problems/maximize-the-distance-between-points-on-a-square/

from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        

    def distance(self, p1: List[int], p2: List[int]) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def sort_points(self, points: List[List[int]]) -> List[List[int]]:
        return sorted(points, key=lambda p: (p[0], p[1]))
    
    # All points lie on the perimeter of the square, so we can represent them as a dict with keys as the points and values as their neighbors
    def getNeighborsDict(self, points: List[List[int]]) -> dict:
        neighbors = {}
        for i in range(len(points)):
            neighbors[tuple(points[i])] = self.getNeighboursOfThisPoint(points, i)
        return neighbors
    
    def getNeighboursOfThisPoint(self, points: List[List[int]], index: int) -> List[List[int]]:
        neighbors = []
        for i in range(len(points)):
            if i != index and self.distance(points[i], points[index]) == 1:
                neighbors.append(points[i])
        return neighbors