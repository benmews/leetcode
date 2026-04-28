from .solution import Solution


def test_example_1():
    assert Solution().minOperations(grid=[[2,4],[6,8]], x=2) == 4


def test_example_2():
    assert Solution().minOperations(grid=[[1,5],[2,3]], x=1) == 5


def test_example_3():
    assert Solution().minOperations(grid=[[1,2],[3,4]], x=2) == -1
