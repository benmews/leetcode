# 788. Rotated Digits
# https://leetcode.com/problems/rotated-digits/


class Solution:
    def rotatedDigits(self, n: int) -> int:
        from functools import lru_cache

        # 0, 1, 8 -> valid, unchanged
        # 2, 5, 6, 9 -> valid, changes
        # 3, 4, 7 -> invalid
        valid = {0, 1, 2, 5, 6, 8, 9}
        change = {2, 5, 6, 9}
        digits = list(map(int, str(n)))

        @lru_cache(maxsize=None)
        def dp(pos, tight, diff, leading_zero):
            if pos == len(digits):
                return int(diff and not leading_zero)
            res = 0
            up = digits[pos] if tight else 9
            for d in range(0, up + 1):
                if d not in valid:
                    continue
                next_tight = tight and (d == up)
                next_diff = diff or (d in change)
                next_leading_zero = leading_zero and (d == 0)
                res += dp(pos + 1, next_tight, next_diff, next_leading_zero)
            return res

        return dp(0, True, False, True)
