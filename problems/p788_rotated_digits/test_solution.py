from .solution import Solution


def test_example_1():
    assert Solution().rotatedDigits(n=10) == 4


def test_example_2():
    assert Solution().rotatedDigits(n=1) == 0


def test_example_3():
    assert Solution().rotatedDigits(n=2) == 1
