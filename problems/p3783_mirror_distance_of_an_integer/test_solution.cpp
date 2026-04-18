#include "solution.cpp"
#include <cassert>
#include <iostream>

int main() {
    Solution s;

    // Example 1
    assert(s.mirrorDistance(25) == 27);
    std::cout << "test_example_1 PASSED\n";

    // Example 2
    assert(s.mirrorDistance(10) == 9);
    std::cout << "test_example_2 PASSED\n";

    // Example 3
    assert(s.mirrorDistance(7) == 0);
    std::cout << "test_example_3 PASSED\n";

    std::cout << "\nAll tests passed!\n";
    return 0;
}
