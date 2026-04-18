// 1848. Minimum Distance to the Target Element
// https://leetcode.com/problems/minimum-distance-to-the-target-element/

#include <algorithm>
#include <numeric>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
public:
    int getMinDistance(const vector<int>& nums, int target, int start) {
        int best = nums.size();
        for (int i = 0; i < static_cast<int>(nums.size()); i++) {
            if (nums[i] == target) {
                best = min(best, abs(i - start));
            }
        }
        return best;
    }
};
