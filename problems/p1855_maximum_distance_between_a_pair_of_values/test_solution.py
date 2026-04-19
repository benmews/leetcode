from .solution import Solution


def test_example_1():
    assert Solution().maxDistance(nums1=[55,30,5,4,2], nums2=[100,20,10,10,5]) == 2


def test_example_2():
    assert Solution().maxDistance(nums1=[2,2,2], nums2=[10,10,1]) == 1


def test_example_3():
    assert Solution().maxDistance(nums1=[30,29,19,5], nums2=[25,25,25,25,25]) == 2
