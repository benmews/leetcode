// 3783. Mirror Distance of an Integer
// https://leetcode.com/problems/mirror-distance-of-an-integer/

#include <algorithm>
#include <numeric>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

class Solution {
public:
    int mirrorDistance(int n) {
        string s = to_string(n);
        string rev(s.rbegin(), s.rend());
        return abs(n - stoi(rev));
    }
};
