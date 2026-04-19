// 1855. Maximum Distance Between a Pair of Values
// https://leetcode.com/problems/maximum-distance-between-a-pair-of-values/

#include <algorithm>
#include <numeric>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
public:
    int maxDistance(vector<int>& nums1, vector<int>& nums2) {
        int j = 0;
        for (int i = 0; i < nums1.size(); ++i) {
            while (i + j < nums2.size() && nums2[i + j] >= nums1[i]) {
                ++j;
            }
        }

        return j > 0 ? j - 1 : 0;
        
    }
};
