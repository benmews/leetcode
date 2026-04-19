#include "solution.cpp"
#include <cassert>
#include <iostream>

int main() {
    Solution s;

    // Example 1
    assert(s.maxDistance({55,30,5,4,2}, {100,20,10,10,5}) == 2);
    std::cout << "test_example_1 PASSED\n";

    // Example 2
    assert(s.maxDistance({2,2,2}, {10,10,1}) == 1);
    std::cout << "test_example_2 PASSED\n";

    // Example 3
    assert(s.maxDistance({30,29,19,5}, {25,25,25,25,25}) == 2);
    std::cout << "test_example_3 PASSED\n";

    std::cout << "\nAll tests passed!\n";
    return 0;
}
