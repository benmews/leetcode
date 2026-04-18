from .solution import Solution


def test_example_1():
    assert Solution().mirrorDistance(n=25) == 27


def test_example_2():
    assert Solution().mirrorDistance(n=10) == 9


def test_example_3():
    assert Solution().mirrorDistance(n=7) == 0
