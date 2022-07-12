from main import fib 


def fib_ans(n: int) -> int:
    if n < 2:
        return n;
    dp = [0 for i in range(n+1)]
    dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[-1]


def test_answer():
    for i in range(72):
        assert fib(i) == fib_ans(i)

if __name__ == "__main__":
    print("Hello, world!")
    print(fib(3))
