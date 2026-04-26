from .solution import Solution


def test_example_1():
    assert Solution().maxDistance(side=2, points=[[0,2],[2,0],[2,2],[0,0]], k=4) == 2


def test_example_2():
    assert Solution().maxDistance(side=2, points=[[0,0],[1,2],[2,0],[2,2],[2,1]], k=4) == 1


def test_example_3():
    assert Solution().maxDistance(side=2, points=[[0,0],[0,1],[0,2],[1,2],[2,0],[2,2],[2,1]], k=5) == 1
