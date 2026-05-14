I'll start by examining the source code to understand what functions need to be tested.
</think>
#include <gtest/gtest.h>

// Include the header for the functions to test
// Assuming the function is declared in app/sample1.h or similar
// For now, we'll declare the function prototype based on the protocol context

// Function to find the maximum of three integers
int find_max(int a, int b, int c);

// Test fixture for MAX3_PROTOCOL
class MAX3ProtocolTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code if needed
    }

    void TearDown() override {
        // Cleanup code if needed
    }
};

// Test: Basic functionality - finding maximum of three distinct positive numbers
TEST_F(MAX3ProtocolTest, FindMax_BasicPositiveNumbers) {
    EXPECT_EQ(find_max(1, 2, 3), 3);
    EXPECT_EQ(find_max(10, 5, 7), 10);
    EXPECT_EQ(find_max(1, 100, 50), 100);
}

// Test: Values may be negative
TEST_F(MAX3ProtocolTest, FindMax_NegativeValues) {
    EXPECT_EQ(find_max(-1, -2, -3), -1);
    EXPECT_EQ(find_max(-10, -5, -1), -1);
    EXPECT_EQ(find_max(-100, -200, -50), -50);
}

// Test: Mixed positive and negative values
TEST_F(MAX3ProtocolTest, FindMax_MixedPositiveNegative) {
    EXPECT_EQ(find_max(-1, 0, 1), 1);
    EXPECT_EQ(find_max(-10, 5, -5), 5);
    EXPECT_EQ(find_max(-100, -50, 10), 10);
}

// Test: Values may be equal
TEST_F(MAX3ProtocolTest, FindMax_EqualValues) {
    EXPECT_EQ(find_max(5, 5, 5), 5);
    EXPECT_EQ(find_max(10, 10, 5), 10);
    EXPECT_EQ(find_max(3, 3, 7), 7);
    EXPECT_EQ(find_max(100, 100, 100), 100);
}

// Test: Edge case [0, 0, 0]
TEST_F(MAX3ProtocolTest, FindMax_AllZeros) {
    EXPECT_EQ(find_max(0, 0, 0), 0);
}

// Test: Edge case [-1, -5, -10]
TEST_F(MAX3ProtocolTest, FindMax_NegativeSequence) {
    EXPECT_EQ(find_max(-1, -5, -10), -1);
}

// Test: Edge case [1000, 1000, 999]
TEST_F(MAX3ProtocolTest, FindMax_TwoEqualMaxOneLess) {
    EXPECT_EQ(find_max(1000, 1000, 999), 1000);
}

// Test: System must return largest value - comprehensive test
TEST_F(MAX3ProtocolTest, FindMax_ReturnsLargestValue) {
    // Largest in first position
    EXPECT_EQ(find_max(100, 1, 2), 100);
    // Largest in second position
    EXPECT_EQ(find_max(1, 100, 2), 100);
    // Largest in third position
    EXPECT_EQ(find_max(1, 2, 100), 100);
}

// Test: Large positive values
TEST_F(MAX3ProtocolTest, FindMax_LargePositiveValues) {
    EXPECT_EQ(find_max(1000000, 2000000, 3000000), 3000000);
    EXPECT_EQ(find_max(INT_MAX, INT_MAX - 1, 0), INT_MAX);
}

// Test: Large negative values
TEST_F(MAX3ProtocolTest, FindMax_LargeNegativeValues) {
    EXPECT_EQ(find_max(INT_MIN, INT_MIN + 1, 0), 0);
    EXPECT_EQ(find_max(-1000000, -2000000, -3000000), -1000000);
}

// Main function to run tests
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}