#include <gtest/gtest.h>

int max3(int a, int b, int c);

TEST(Max3Test, BasicCases) {
    EXPECT_EQ(max3(3, 2, 1), 3);   // a is largest
    EXPECT_EQ(max3(1, 5, 2), 5);   // b is largest
    EXPECT_EQ(max3(1, 2, 7), 7);   // c is largest
}

TEST(Max3Test, EdgeCases) {
    EXPECT_EQ(max3(-1, -2, -3), -1);
    EXPECT_EQ(max3(5, 5, 3), 5);
}
