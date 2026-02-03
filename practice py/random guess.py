import random

# 1. Random integer in a range [a, b]
a, b = 1, 100
rand_int = random.randint(a, b)
print("Random integer between", a, "and", b, "=", rand_int)

# 2. Random float in [0.0, 1.0)
rand_float = random.random()
print("Random float [0.0, 1.0) =", rand_float)

# 3. Random choice from a list
choices = ['apple', 'banana', 'mango', 'orange']
pick = random.choice(choices)
print("Random choice =", pick)

# 4. Shuffle a list in-place
nums = list(range(1, 11))
random.shuffle(nums)
print("Shuffled list:", nums)

# 5. Random sample (k distinct elements)
sample_3 = random.sample(choices, 2)
print("Random sample:", sample_3)