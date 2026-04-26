from .solution import Solution


def test_example_1():
    assert Solution().furthestDistanceFromOrigin(moves="L_RL__R") == 3


def test_example_2():
    assert Solution().furthestDistanceFromOrigin(moves="_R__LL_") == 5


def test_example_3():
    assert Solution().furthestDistanceFromOrigin(moves="_______") == 7
