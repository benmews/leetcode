from .solution import Solution


def test_example_1():
    assert Solution().maxPathScore(grid=[[0, 1],[2, 0]], k=1) == 2


def test_example_2():
    assert Solution().maxPathScore(grid=[[0, 1],[1, 2]], k=1) == -1
