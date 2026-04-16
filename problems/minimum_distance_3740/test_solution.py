from .solution import Solution

def test_basic_case():
    nums = [1,2,1,1,3]
    assert Solution().minimum_distance(nums) == 6

def test_two_number_case():
    nums = [1,1,2,3,2,1,2]
    assert Solution().minimum_distance(nums) == 8

def test_neg_case():
    nums = [1]
    assert Solution().minimum_distance(nums) == -1

def test_edge_case():
    nums = [3,3,3]
    assert Solution().minimum_distance(nums) == 4
