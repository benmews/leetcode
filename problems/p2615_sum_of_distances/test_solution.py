from .solution import Solution


def test_example_1():
    assert Solution().distance(nums=[1,3,1,1,2]) == [5,0,3,4,0]


def test_example_2():
    assert Solution().distance(nums=[0,5,3]) == [0,0,0]
