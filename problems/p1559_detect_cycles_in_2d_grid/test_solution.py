from .solution import Solution


def test_example_1():
    assert Solution().containsCycle(grid=[["a","a","a","a"],["a","b","b","a"],["a","b","b","a"],["a","a","a","a"]]) == True


def test_example_2():
    assert Solution().containsCycle(grid=[["c","c","c","a"],["c","d","c","c"],["c","c","e","c"],["f","c","c","c"]]) == True


def test_example_3():
    assert Solution().containsCycle(grid=[["a","b","b"],["b","z","b"],["b","b","a"]]) == False
