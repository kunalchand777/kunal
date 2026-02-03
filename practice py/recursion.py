# factorial_recursion.py
def factorial(n):
    """Return n! for n >= 0 using recursion. Raises ValueError for negative n."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    for x in [0, 1, 5, 7]:
        print(f"{x}! = {factorial(x)}")