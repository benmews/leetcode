from .solution import Solution


def test_example_1():
    assert Solution().hasValidPath(grid=[[2,4,3],[6,5,2]]) == True


def test_example2():
    assert Solution().hasValidPath(grid=[[1,2,1],[1,2,1]]) == False



def test_example_3():
    assert Solution().hasValidPath(grid=[[1,1,2]]) == False
