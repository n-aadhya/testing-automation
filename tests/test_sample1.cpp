#include "sample1.cpp"
#include <gtest/gtest.h>

TEST(LargestValueTest, MaxOfEqualValues) {
    int def = 0;
    EXPECT_EQ(max3(def, def, def), def);
    int high = 1000;
    EXPECT_EQ(max3(high, high, high), high);
    int neg = -1;
    EXPECT_EQ(max3(neg, neg, neg), neg);
}

TEST(LargestValueTest, MaxOfMixedValues) {
    EXPECT_EQ(max3(5, 3, 9), 9);
    EXPECT_EQ(max3(-2, -5, -1), -1);
    EXPECT_EQ(max3(-10, 0, -3), 0);
    EXPECT_EQ(max3(100, -5, 100), 100);
    EXPECT_EQ(max3(-1, -5, -1), -1);
}

TEST(LargestValueTest, EdgeCases) {
    EXPECT_EQ(max3(0, 0, 0), 0);
    EXPECT_EQ(max3(-1, -5, -10), -1);
    EXPECT_EQ(max3(1000, 1000, 999), 1000);
}