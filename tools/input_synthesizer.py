import random


def generate_inputs_from_conditions(conditions, num_tests):
    inputs = []

    # 🔥 HARD-CODED PATH COVERAGE (guaranteed)
    inputs.extend([
        (10, 5, 1, 10),   # a > b && a > c
        (1, 10, 5, 10),   # b > c && b > a
        (1, 5, 10, 10),   # c > a && c > b
        (5, 5, 5, 5),     # equal case
        (-1, -5, -10, -1) # negative values
    ])

    # 🔥 MUTATION STRATEGY (this is key)
    for _ in range(num_tests):
        base = random.choice(inputs)

        a = base[0] + random.randint(-3, 3)
        b = base[1] + random.randint(-3, 3)
        c = base[2] + random.randint(-3, 3)

        inputs.append((a, b, c, max(a, b, c)))

    return inputs[:num_tests]
