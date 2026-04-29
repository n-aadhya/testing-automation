
#include <gtest/gtest.h>

int max3(int, int, int);

TEST(AutoTest, Case1) {
    EXPECT_EQ(max3(10, 5, 1), 10);
}

TEST(AutoTest, Case2) {
    EXPECT_EQ(max3(1, 10, 5), 10);
}

TEST(AutoTest, Case3) {
    EXPECT_EQ(max3(1, 5, 10), 10);
}

TEST(AutoTest, Case4) {
    EXPECT_EQ(max3(5, 5, 5), 5);
}

TEST(AutoTest, Case5) {
    EXPECT_EQ(max3(-1, -5, -10), -1);
}

TEST(AutoTest, Case6) {
    EXPECT_EQ(max3(11, 5, -1), 11);
}

TEST(AutoTest, Case7) {
    EXPECT_EQ(max3(3, 2, 10), 10);
}

TEST(AutoTest, Case8) {
    EXPECT_EQ(max3(0, 2, 8), 8);
}

TEST(AutoTest, Case9) {
    EXPECT_EQ(max3(2, 8, 7), 8);
}

TEST(AutoTest, Case10) {
    EXPECT_EQ(max3(6, 6, 3), 6);
}

TEST(AutoTest, Case11) {
    EXPECT_EQ(max3(12, 3, -1), 12);
}

TEST(AutoTest, Case12) {
    EXPECT_EQ(max3(-2, 7, 8), 8);
}

TEST(AutoTest, Case13) {
    EXPECT_EQ(max3(9, 5, -1), 9);
}

TEST(AutoTest, Case14) {
    EXPECT_EQ(max3(8, 5, 3), 8);
}

TEST(AutoTest, Case15) {
    EXPECT_EQ(max3(8, 4, -1), 8);
}
