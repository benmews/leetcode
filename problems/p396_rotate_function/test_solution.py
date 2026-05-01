from .solution import Solution


def test_example_1():
    assert Solution().maxRotateFunction(nums=[4,3,2,6]) == 26


def test_example_2():
    assert Solution().maxRotateFunction(nums=[100]) == 0
