#include "solution.cpp"
#include <cassert>
#include <iostream>

int main() {
    Solution s;

    // Example 1
    assert(s.getMinDistance({1,2,3,4,5}, 5, 3) == 1);
    std::cout << "test_example_1 PASSED\n";

    // Example 2
    assert(s.getMinDistance({1}, 1, 0) == 0);
    std::cout << "test_example_2 PASSED\n";

    // Example 3
    assert(s.getMinDistance({1,1,1,1,1,1,1,1,1,1}, 1, 0) == 0);
    std::cout << "test_example_3 PASSED\n";

    std::cout << "\nAll tests passed!\n";
    return 0;
}
