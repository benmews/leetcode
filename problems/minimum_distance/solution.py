from typing import List

class Solution:
    def minimum_distance(self, nums: List[int]) -> int:
        smallestDist = -1
        indexesOfValue = self.getIndexesOfValue(nums)
        for val in range(len(nums)):
            distancesOfValue = self.getDistOfValue(indexesOfValue[val]);
            if len(distancesOfValue) == 0 :
                smallestOfValue = -1;
            else:
                smallestOfValue = min(distancesOfValue);
            if smallestOfValue != -1 and (smallestOfValue < smallestDist or smallestDist == -1):
                smallestDist = smallestOfValue;
        return smallestDist;

    def getIndexesOfValue(self, nums: List[int]):
        asdf = [];
        qwer = range(len(nums));
        for val in qwer:
            asdf.append( [i for (i,v) in enumerate(nums) if v == val+1]);
        return asdf;

    def getDistOfValue(self, ind: List[int]):
        dists = [];
        for (i, v1) in enumerate(ind):
            if i != 0 and i != 1:
                v2 = ind[i-1];
                v3 = ind[i-2];
                dist = abs(v1-v2) + abs(v2-v3) + abs(v3-v1);
                dists.append(dist);
        return dists;
