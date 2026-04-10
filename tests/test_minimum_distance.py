from problems.minimum_distance import Solution


def test_basic_case():
    nums = [1, 3, 6, 10]
    assert Solution().minimum_distance(nums) == 2


def test_single_element():
    assert Solution().minimum_distance([5]) == 0


def test_empty():
    assert Solution().minimum_distance([]) == 0


def test_negative_numbers():
    nums = [-10, -3, 0, 4]
    assert Solution().minimum_distance(nums) == 3
