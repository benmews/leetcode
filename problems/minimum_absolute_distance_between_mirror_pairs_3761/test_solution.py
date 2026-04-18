from .solution import Solution


def test_example_1():
    assert Solution().minMirrorPairDistance(nums=[12,21,45,33,54]) == 1;


def test_example_2():
    assert Solution().minMirrorPairDistance(nums=[120,21]) == 1;


def test_example_3():
    assert Solution().minMirrorPairDistance(nums=[21,120]) == -1;