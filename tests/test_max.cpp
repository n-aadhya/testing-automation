#include <gtest/gtest.h>

// declare function
int max2(int a, int b);

TEST(MaxTest, BasicCases) {
    EXPECT_EQ(max2(2, 3), 3);
    EXPECT_EQ(max2(5, 1), 5);
}

TEST(MaxTest, NegativeCases) {
    EXPECT_EQ(max2(-1, -2), -1);
}
