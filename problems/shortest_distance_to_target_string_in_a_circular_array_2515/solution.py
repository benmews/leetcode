# 2515. Shortest Distance to Target String in a Circular Array
# https://leetcode.com/problems/shortest-distance-to-target-string-in-a-circular-array/

from typing import List


class Solution:
    def closestTarget(self, words: List[str], target: str, startIndex: int) -> int:
        indexes = [i for i, w in enumerate(words) if w == target];
        if len(indexes) == 0:
            return -1;
        smallestDist = -1;
        for i in indexes:
            dist = min(abs(i-startIndex), abs(i+len(words)-startIndex), abs(i-len(words)-startIndex));
            if dist < smallestDist or smallestDist == -1:
                smallestDist = dist;
        return smallestDist;
