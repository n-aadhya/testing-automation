num = int(input("Enter a number: "))

# Decision Path 1
if num < 0:
    print("Negative number")

# Decision Path 2
elif num == 0:
    print("Zero entered")

# Decision Path 3
elif num % 2 == 0:
    print("Positive even number")

    # Loop
    for i in range(1, 4):
        print("Loop iteration:", i)

# Decision Path 4
else:
    print("Positive odd number")

    count = 0

    # While loop
    while count < 3:
        print("Count =", count)
        count += 1

print("Program finished")
