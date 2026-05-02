# 788. Rotated Digits
# https://leetcode.com/problems/rotated-digits/


class Solution:
    def rotatedDigits(self, n: int) -> int:
        nos = ["3", "4", "7"]
        yess = ["2", "5", "6", "9"]
        # don't matter: 0, 1, 8

        count = 0
        for i in range(n + 1):
            if not any(no in str(i) for no in nos) and any(
                yes in str(i) for yes in yess
            ):
                count += 1

        return count
