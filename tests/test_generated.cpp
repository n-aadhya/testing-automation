
#include <gtest/gtest.h>

int max3(int a, int b, int c);

TEST(AutoTest, Case1) {
    EXPECT_EQ(max3(5, 2, 1), 5);
}

TEST(AutoTest, Case2) {
    EXPECT_EQ(max3(1, 6, 2), 6);
}

TEST(AutoTest, Case3) {
    EXPECT_EQ(max3(1, 2, 7), 7);
}

TEST(AutoTest, Case4) {
    EXPECT_EQ(max3(5, 5, 5), 5);
}
