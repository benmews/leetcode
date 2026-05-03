from .solution import Solution

# def test_example_1():
#     assert Solution().rotateString(s="abcde", goal="cdeab")


# def test_example_2():
#     assert not Solution().rotateString(s="abcde", goal="abced")


def test_example_3():
    assert Solution().rotateString(s="gcmbf", goal="fgcmb")
