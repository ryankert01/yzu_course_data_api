

def fib(n: int) -> int:
    golden_ratio = (1 + 5 ** 0.5) / 2
    return int((golden_ratio ** n + 1) / 5 ** 0.5)


