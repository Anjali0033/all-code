def fibonacci(n):
    MOD = 1000000007
    
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Initialize variables for F(0) and F(1)
    a, b = 0, 1
    
    # Compute Fibonacci sequence iteratively
    for _ in range(2, n + 1):
        a, b = b, (a + b) % MOD
    
    return b

# Example usage:
N = 5
print(fibonacci(N))  # Output: 5
