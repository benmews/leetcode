from .solution import Solution


def test_example_1():
    assert Solution().maxDistance(colors=[1,1,1,6,1,1,1]) == 3


def test_example_2():
    assert Solution().maxDistance(colors=[1,8,3,8,3]) == 4


def test_example_3():
    assert Solution().maxDistance(colors=[0,1]) == 1
