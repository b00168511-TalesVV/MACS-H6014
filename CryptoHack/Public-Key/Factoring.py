import sympy

# Given 150-bit number
n = 510143758735509025530880200653196460532653147

# Factor the number using sympy's factorint
factors = sympy.factorint(n)

# Extract and sort the prime factors
primes = sorted(factors.keys())

# Display the results
print("All prime factors:", primes)
print("Smaller prime factor:", primes[0])
