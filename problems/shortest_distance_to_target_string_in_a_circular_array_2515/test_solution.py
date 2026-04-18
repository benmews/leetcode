from .solution import Solution


def test_example_1():
    assert Solution().closestTarget(words=["hello","i","am","leetcode","hello"], target="hello", startIndex=1) == 1


def test_example_2():
    assert Solution().closestTarget(words=["a","b","leetcode"], target="leetcode", startIndex=0) == 1


def test_example_3():
    assert Solution().closestTarget(words=["i","eat","leetcode"], target="ate", startIndex=0) == -1
