# 796. Rotate String
# https://leetcode.com/problems/rotate-string/


class Solution:

    def rotateString(self, s: str, goal: str) -> bool:
        if len(s) != len(goal) or set(s) != set(goal):
            return False
        for i in range(len(s)):
            rotated = s[i:] + s[:i]
            if goal == rotated:
                return True
        return False

    def rotateStringSimple(self, s: str, goal: str) -> bool:
        return len(s) == len(goal) and goal in (s + s)

    def rotateStringKMP(self, s: str, goal: str) -> bool:
        # KMP helper to build prefix table
        def build_lps(pattern):
            lps = [0] * len(pattern)
            length = 0
            i = 1
            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1
            return lps

        if len(s) != len(goal):
            return False
        concat = s + s
        lps = build_lps(goal)
        i = j = 0
        while i < len(concat):
            if concat[i] == goal[j]:
                i += 1
                j += 1
                if j == len(goal):
                    # Found match
                    return True
            else:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return False
