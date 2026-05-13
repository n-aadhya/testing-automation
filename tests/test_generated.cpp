
#include <gtest/gtest.h>

int max3(int, int, int);

TEST(AutoTest, Case1) {
    EXPECT_EQ(max3(0, 0, 0), 0);
}

TEST(AutoTest, Case2) {
    EXPECT_EQ(max3(-1, -5, -10), -1);
}

TEST(AutoTest, Case3) {
    EXPECT_EQ(max3(1000, 1000, 999), 1000);
}

TEST(AutoTest, Case4) {
    EXPECT_EQ(max3(0, 0, 0), 0);
}
