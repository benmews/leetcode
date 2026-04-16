from .solution import Solution


def test_example_1():
    assert Solution().getMinDistance(nums=[1,2,3,4,5], target=5, start=3) == 1


def test_example_2():
    assert Solution().getMinDistance(nums=[1], target=1, start=0) == 0


def test_example_3():
    assert Solution().getMinDistance(nums=[1,1,1,1,1,1,1,1,1,1], target=1, start=0) == 0
